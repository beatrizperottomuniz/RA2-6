'''
Integrantes do grupo (ordem alfabética):
Beatriz Perotto Muniz - @beatrizperottomuniz

Nome do grupo no Canvas: RA2 6
'''
# simula o pipeline completo: léxico - lerTokens - construirGramatica - parsear - gerarArvore - gerarAssembly

import unittest
import os
import json
import globalVars
from Token import TokenType
from leituraArquivo import lerArquivo
from analisadorLexico import parseExpressao
from leTokens import lerTokens
from construirGramatica import construirGramatica
from parsear import parsear
from gerarArvore import gerarArvore
from gerarAssembly import gerarAssembly

tabela              = construirGramatica()['tabela']
arquivo_tks_temp = "_tokens_e2e_novo.txt"
arquivo_asm_temp    = "saida2.s"
arquivo_fonte_temp  = "_fonte_e2e_novo.txt"


def resetar():
    globalVars.string_pool_global.pool.clear()
    globalVars.string_pool_global.strings.clear()
    globalVars.contador_linha_global = 1
    globalVars.total_linhas_global   = 1


def rodarLexico(caminho):
    linhas = []
    lerArquivo(caminho, linhas)
    globalVars.total_linhas_global = len(linhas)
    tokens_lista = []
    tem_erro = False
    for linha in linhas:
        tokens_linha = []
        parseExpressao(linha, tokens_linha)
        tokens_lista.extend(tokens_linha)
        if any(t.tipo == TokenType.UNKNOWN for t in tokens_linha):
            tem_erro = True
        globalVars.contador_linha_global += 1
    dados = {
        "string_pool": globalVars.string_pool_global.strings,
        "tokens": [{"tipo": t.tipo, "linha": t.linha,
                    "coluna": t.coluna, "simbolo_id": t.simbolo_id}
                   for t in tokens_lista]
    }
    with open(arquivo_tks_temp, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)
    return tem_erro


def rodarPipeline(caminho_fonte):
    resetar()
    tem_erro_lexico = rodarLexico(caminho_fonte)
    resetar()
    tokens = lerTokens(arquivo_tks_temp)
    resultado = parsear(tokens, tabela)
    erros = resultado['erros']
    arvore, asm_texto = None, ""
    if not erros and not tem_erro_lexico:
        arvore = gerarArvore(resultado['estrutura_derivacao'])
        gerarAssembly(arvore)
        if os.path.exists(arquivo_asm_temp):
            with open(arquivo_asm_temp, encoding='utf-8') as f:
                asm_texto = f.read()
    return arvore, asm_texto, erros, tem_erro_lexico


def criarFonte(expressoes):
    with open(arquivo_fonte_temp, 'w') as f:
        f.write("(START)\n")
        for e in expressoes:
            f.write(e + "\n")
        f.write("(END)\n")


def limpar():
    for f in [arquivo_tks_temp, arquivo_fonte_temp,arquivo_asm_temp,
              'saida_arvore.txt', 'saida_arvore_json.txt',
              'saida_arvore.md',  'saida_arvore.png']:
        if os.path.exists(f):
            os.remove(f)
    resetar()


def encontrarNos(no, tipo):
    resultado = []
    if no.tipo == tipo:
        resultado.append(no)
    for filho in no.filhos:
        resultado.extend(encontrarNos(filho, tipo))
    return resultado


def temTerminal(no, tipo_token):
    if no.token and no.token.tipo == tipo_token:
        return True
    return any(temTerminal(f, tipo_token) for f in no.filhos)


_PROGRAMA_E2E = [
    "(10 A)",                                    # 1 – atribuição
    "(3 4 +)",                                   # 2 – adição
    "(10 3 -)",                                  # 3 – subtração
    "(2 5 *)",                                   # 4 – multiplicação
    "(8 2 |)",                                   # 5 – divisão real
    "(9 3 /)",                                   # 6 – divisão inteira
    "(10 3 %)",                                  # 7 – módulo
    "(2 3 ^)",                                   # 8 – potenciação
    "(3.14 2.0 +)",                              # 9 – float
    "((A) 5.0 *)",                               # 10 – leitura de variável
    "((5 5 ==) (1 2 +) IF)",                     # 11 – IF com ==
    "(3 (1 2 +) FOR)",                           # 12 – FOR
    "(1 RES)",                                   # 13 – RES
    "((10 5 >) (3 2 -) IF)",                     # 14 – IF com >
    "((2 3 +) (4 5 *) -)",                       # 15 – aninhamento
]


class TestPipelineCompleto(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        criarFonte(_PROGRAMA_E2E)
        cls.arvore, cls.asm, cls.erros, cls.erro_lexico = rodarPipeline(arquivo_fonte_temp)

    @classmethod
    def tearDownClass(cls):
        limpar()

    # -- léxico e sintático --

    def test_sem_erro_lexico(self):
        self.assertFalse(self.erro_lexico)

    def test_sem_erro_sintatico(self):
        self.assertEqual(self.erros, [])

    # -- árvore: estrutura --

    def test_arvore_criada(self):
        self.assertIsNotNone(self.arvore)

    def test_arvore_raiz_prog(self):
        self.assertEqual(self.arvore.tipo, 'prog')

    def test_arvore_tem_list_stmts(self):
        self.assertTrue(len(encontrarNos(self.arvore, 'list_stmts')) > 0)

    def test_arvore_tem_rpn(self):
        self.assertTrue(len(encontrarNos(self.arvore, 'rpn')) > 0)

    # -- árvore: conteúdo --

    def test_arvore_tem_if(self):
        self.assertTrue(temTerminal(self.arvore, 'KEYWORD_IF'))

    def test_arvore_tem_for(self):
        self.assertTrue(temTerminal(self.arvore, 'KEYWORD_FOR'))

    def test_arvore_tem_res(self):
        self.assertTrue(temTerminal(self.arvore, 'KEYWORD_RES'))

    def test_arvore_tem_floats(self):
        self.assertTrue(temTerminal(self.arvore, 'NUM_FLOAT'))

    # -- arquivos de saída --

    def test_arvore_txt_gerado(self):
        self.assertTrue(os.path.exists('saida_arvore.txt'))

    def test_arvore_json_gerado(self):
        self.assertTrue(os.path.exists('saida_arvore_json.txt'))

    def test_arvore_json_valido(self):
        #saida_arvore_json.txt deve ser JSON válido com chave 'arvore'
        with open('saida_arvore_json.txt', encoding='utf-8') as f:
            dados = json.load(f)
        self.assertIn('arvore', dados)

    # -- assembly: estrutura obrigatória --

    def test_assembly_gerado(self):
        self.assertTrue(os.path.exists(arquivo_asm_temp))

    def test_assembly_tem_data(self):
        self.assertIn(".data", self.asm)

    def test_assembly_tem_text(self):
        self.assertIn(".text", self.asm)

    def test_assembly_tem_start(self):
        self.assertIn("_start:", self.asm)

    def test_assembly_tem_fpu(self):
        self.assertIn("FPEXC", self.asm)

    def test_assembly_tem_uart(self):
        self.assertIn("UART_PUTCHAR", self.asm)

    def test_assembly_tem_print(self):
        self.assertIn("PRINT_RES_HEX", self.asm)

    # -- assembly: conteúdo --

    def test_assembly_tem_if_label(self):
        self.assertIn("IF_FALSE", self.asm)

    def test_assembly_tem_for_loop(self):
        self.assertIn("FOR_LOOP", self.asm)

    def test_assembly_tem_for_ctr(self):
        self.assertIn("FOR_CTR", self.asm)

    def test_assembly_tem_variavel(self):
        self.assertIn("A_MEM", self.asm)

    def test_assembly_tem_res_linhas(self):
        #15 expressões — deve ter RES_LINHA_1 até RES_LINHA_15
        for i in range(1, 16):
            with self.subTest(linha=i):
                self.assertIn(f"RES_LINHA_{i}", self.asm)

    def test_assembly_instrucoes_ieee754(self):
        #Operações devem usar registradores F64 (double precision)
        self.assertIn(".F64", self.asm)


class TestAssemblyPorOperacao(unittest.TestCase):

    def tearDown(self):
        limpar()

    def _asm(self, expr):
        criarFonte([expr])
        _, asm, _, _ = rodarPipeline(arquivo_fonte_temp)
        return asm

    def test_adicao_vadd(self):
        self.assertIn("VADD.F64", self._asm("(3 4 +)"))

    def test_subtracao_vsub(self):
        self.assertIn("VSUB.F64", self._asm("(10 3 -)"))

    def test_multiplicacao_vmul(self):
        self.assertIn("VMUL.F64", self._asm("(3 4 *)"))

    def test_divisao_real_vdiv(self):
        self.assertIn("VDIV.F64", self._asm("(8 2 |)"))

    def test_divisao_inteira_vcvt(self):
        self.assertIn("VCVT.S32.F64", self._asm("(9 3 /)"))

    def test_modulo_vsub_final(self):
        self.assertIn("VSUB.F64", self._asm("(10 3 %)"))

    def test_potenciacao_pow_loop(self):
        self.assertIn("POW_LOOP", self._asm("(2 3 ^)"))

    def test_relacional_vcmp(self):
        self.assertIn("VCMP.F64", self._asm("((5 5 ==) (1 2 +) IF)"))

    def test_if_beq(self):
        self.assertIn("BEQ", self._asm("((5 5 ==) (1 2 +) IF)"))

    def test_for_sub_contador(self):
        self.assertIn("SUB r2, r2, #1", self._asm("(3 (1 2 +) FOR)"))

    def test_atribuicao_vstr(self):
        self.assertIn("VSTR", self._asm("(10 X)"))

    def test_leitura_vldr(self):
        criarFonte(["(5 X)", "(X)"])
        _, asm, _, _ = rodarPipeline(arquivo_fonte_temp)
        self.assertIn("VLDR", asm)

    def test_res_add_sp(self):
        criarFonte(["(3 4 +)", "(1 RES)"])
        _, asm, _, _ = rodarPipeline(arquivo_fonte_temp)
        self.assertIn("ADD sp, sp, #8", asm)


class TestArvorePorOperacao(unittest.TestCase):

    def tearDown(self):
        limpar()

    def _arvore(self, expr):
        criarFonte([expr])
        arvore, _, _, _ = rodarPipeline(arquivo_fonte_temp)
        return arvore

    def test_adicao_tem_plus(self):
        self.assertTrue(temTerminal(self._arvore("(3 4 +)"), 'PLUS'))

    def test_if_tem_keyword_if(self):
        self.assertTrue(temTerminal(self._arvore("((5 5 ==) (1 2 +) IF)"), 'KEYWORD_IF'))

    def test_for_tem_keyword_for(self):
        self.assertTrue(temTerminal(self._arvore("(3 (1 2 +) FOR)"), 'KEYWORD_FOR'))

    def test_res_tem_keyword_res(self):
        criarFonte(["(3 4 +)", "(1 RES)"])
        arvore, _, _, _ = rodarPipeline(arquivo_fonte_temp)
        self.assertTrue(temTerminal(arvore, 'KEYWORD_RES'))

    def test_aninhamento_expande_stmt(self):
        arvore = self._arvore("((3 2 +) 4 *)")
        self.assertTrue(len(encontrarNos(arvore, 'stmt')) > 0)

    def test_raiz_sempre_prog(self):
        arvore = self._arvore("(3 4 +)")
        self.assertEqual(arvore.tipo, 'prog')


class TestPipelineComErros(unittest.TestCase):

    def tearDown(self):
        limpar()

    def test_erro_lexico_nao_gera_assembly(self):
        #Token inválido — pipeline retorna erro léxico e sem assembly
        criarFonte(["(3 & 4)"])
        _, asm, _, erro_lexico = rodarPipeline(arquivo_fonte_temp)
        self.assertTrue(erro_lexico)
        self.assertEqual(asm, "")   # rodarPipeline não lê assembly se houve erro

    def test_erro_sintatico_nao_gera_assembly(self):
        #Erro sintático — pipeline retorna erros e sem assembly
        criarFonte(["(+ 3 4)"])
        _, asm, erros, _ = rodarPipeline(arquivo_fonte_temp)
        self.assertTrue(len(erros) > 0)
        self.assertEqual(asm, "")   # rodarPipeline não lê assembly se houve erro

    def test_erro_sintatico_tem_linha(self):
        #Mensagem de erro deve indicar a linha
        criarFonte(["(+ 3 4)"])
        _, _, erros, _ = rodarPipeline(arquivo_fonte_temp)
        self.assertTrue(any('linha' in e.lower() for e in erros))


if __name__ == '__main__':
    unittest.main()
