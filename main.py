'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import sys
import json
from Token import TokenType
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
from geradorAssembly import gerarAssembly
from executaExpressao import executarExpressao
from exibeResultados import exibirResultados

import globalVars

def exportarTokens(lista_tokens, caminho_exportar="saida_tokens.txt"):
    tokens_serializados = []
    # token -> dicionario
    for token in lista_tokens:
        tokens_serializados.append({
            "tipo": token.tipo,
            "linha": token.linha,
            "coluna": token.coluna,
            "simbolo_id": token.simbolo_id
        })
    # tokens + string pool
    dados = {
        "string_pool": globalVars.string_pool_global.strings,
        "tokens": tokens_serializados
    }

    try:
        with open(caminho_exportar, 'w', encoding='utf-8') as file:
            json.dump(dados, file, indent=4, ensure_ascii=False)
        print(f"Tokens exportados para o arquivo: '{caminho_exportar}'")
    except Exception as e:
        print(f"Falha ao salvar o arquivo de tokens: {e}")

''' não inserido no analisador léxico pois é de responsabilidade de outra etapa; inserido por requisição em seção 26.3 :
"(...) Entradas inválidas (ex.: (3.14 2.0 &), números malformados como 3.14.5, 3,45 ou parênteses desbalanceados). (...)"
'''
def verificacaoParentesesDesbalanceados(linha: str) -> bool:
    pilha = []
    for char in linha:
        if char == '(':
            pilha.append(char)
        elif char == ')':
            if not pilha:
                return False
            pilha.pop()
    return not pilha

# ------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <nome_do_arquivo>.txt")
        sys.exit(1)

    caminho = sys.argv[1]
    linhas = []
    tokens_lista = []
    linhas_assembly = []
    resultados = []
    memoria = {}
    erro_linha = False
    

    lerArquivo(caminho, linhas)
    globalVars.total_linhas_global = len(linhas)
    for linha in linhas:
        #print(linha)
        tokens_linha = []
        parseExpressao(linha, tokens_linha)
        tokens_lista.extend(tokens_linha) # lista para exportar

        token_desconhecido_na_linha = [token for token in tokens_linha if token.tipo == TokenType.UNKNOWN]
        if token_desconhecido_na_linha:
            erro_linha = True

        if not verificacaoParentesesDesbalanceados(linha):
            print(f"Erro na linha {globalVars.contador_linha_global}: parênteses desbalanceados\n")
            erro_linha = True

        if not erro_linha :
            executarExpressao(tokens_linha, resultados , memoria)
            gerarAssembly(tokens_linha, linhas_assembly)

        globalVars.contador_linha_global += 1

    exportarTokens(tokens_lista)

    if erro_linha :
        print ("\nERRO : O código fonte possui um erro, não será possível gerar código assembly")
    else:
        exibirResultados(resultados)
        print("\nSUCESSO: Arquivo 'saida.s' gerado com sucesso!")