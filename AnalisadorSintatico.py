'''
Integrantes do grupo:
Beatriz Perotto Muniz - @beatrizperottomuniz

Nome do grupo no Canvas: RA2 6
'''
import sys
import os
import json
from Token import Token, TokenType
import globalVars
# lexico
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
# sintatico
from leTokens import lerTokens
from construirGramatica import construirGramatica
from parsear import parsear
from gerarArvore import gerarArvore
from gerarAssembly import gerarAssembly
# from executaExpressao import executarExpressao
from exibeResultados import exibirResultados

ARQUIVO_TOKENS = "saida_tokens_2.txt"


# funcs lexico


def _exportar_tokens(lista_tokens, caminho=ARQUIVO_TOKENS):
    tokens_serializados = []
    for token in lista_tokens:
        tokens_serializados.append({
            "tipo": token.tipo,
            "linha": token.linha,
            "coluna": token.coluna,
            "simbolo_id": token.simbolo_id
        })
    dados = {
        "string_pool": globalVars.string_pool_global.strings,
        "tokens": tokens_serializados
    }
    try:
        with open(caminho, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print(f"Tokens exportados para '{caminho}'")
    except Exception as e:
        print(f"Erro ao salvar tokens: {e}")


def _rodar_lexico(caminho_fonte):
    #Executa o analisador léxico no arquivo fonte e salva saida_tokens.txt ret True se não houve erros
    linhas = []
    lerArquivo(caminho_fonte, linhas)
    globalVars.total_linhas_global = len(linhas)

    tokens_lista = []
    erro = False

    for linha in linhas:
        tokens_linha = []
        parseExpressao(linha, tokens_linha)
        tokens_lista.extend(tokens_linha)

        if any(t.tipo == TokenType.UNKNOWN for t in tokens_linha):
            print(f"Erro léxico na linha {globalVars.contador_linha_global}: token desconhecido")
            erro = True

        globalVars.contador_linha_global += 1

    if not erro:
        _exportar_tokens(tokens_lista)

    return not erro


# divide tokens por instrucao

def _extrair_instrucoes(tokens):
#   Divide a lista plana de tokens em grupos por instrução, ignorando (START), (END) e EOF.
    instrucoes = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t.tipo == TokenType.EOF:
            break
        if t.tipo == TokenType.LPAREN:
            proximo = tokens[i + 1].tipo if i + 1 < len(tokens) else None
            if proximo in (TokenType.KEYWORD_START, TokenType.KEYWORD_END):
                # pula o grupo inteiro (START) ou (END)
                while i < len(tokens) and tokens[i].tipo != TokenType.RPAREN:
                    i += 1
                i += 1
                continue
            # coleta grupo completo rastreando profundidade de parênteses
            grupo = []
            depth = 0
            while i < len(tokens):
                grupo.append(tokens[i])
                if tokens[i].tipo == TokenType.LPAREN:
                    depth += 1
                elif tokens[i].tipo == TokenType.RPAREN:
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            instrucoes.append(grupo)
        else:
            i += 1
    return instrucoes


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 analisadorSintatico.py <arquivo>.txt")
        sys.exit(1)

    caminho = sys.argv[1]

    # 1. léxico — só roda se saida_tokens.txt não existir
    if not os.path.exists(ARQUIVO_TOKENS):
        print(f"'{ARQUIVO_TOKENS}' não encontrado — rodando analisador léxico...")
        if not _rodar_lexico(caminho):
            print("\nERRO léxico — execução interrompida.")
            sys.exit(1)
    else:
        print(f"'{ARQUIVO_TOKENS}' encontrado — pulando analisador léxico.")

    # 2. ler tokens
    tokens = lerTokens(ARQUIVO_TOKENS)

    # 3. gramática e tabela LL(1)
    resultado_gramatica = construirGramatica()
    tabela = resultado_gramatica['tabela']

    # 4. parsing
    resultado_parser = parsear(tokens, tabela)

    if resultado_parser['erros']:
        print("\n------ Erros sintáticos ------")
        for erro in resultado_parser['erros']:
            print(f"  {erro}")
        print("------------------------------")
        print("\nERRO sintático — execução interrompida.")
        sys.exit(1)

    print("Análise sintática: OK")

    # 5. árvore sintática
    arvore = gerarArvore(resultado_parser['estrutura_derivacao'])
    print("Árvore gerada: saida_arvore.json / saida_arvore.txt / saida_arvore.png")

    # 6. geração de assembly
    gerarAssembly(arvore)
    print("Assembly gerado: saida2.s")

    # 7. interpretador — executa cada instrução e exibe resultados
    # instrucoes = _extrair_instrucoes(tokens)
    # resultados = []
    # memoria    = {}
    # for instrucao in instrucoes:
    #     executarExpressao(instrucao, resultados, memoria)

    # exibirResultados(resultados)
