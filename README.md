# RA2-6
### Analisador Sintático
**Instituição** : PUCPR - Pontifícia Universidade Católica do Paraná<br>
**Disciplina** : Linguagens Formais e Compiladores (Turma 9º U) - Engenharia de Computação (Noite) - 2026 / 1º Sem <br>
**Professor** : Frank Coelho de Alcantara<br>
**Aluna** : Beatriz Perotto Muniz [@beatrizperottomuniz](https://github.com/beatrizperottomuniz)<br>

### Descrição
Este projeto implementa um analisador sintático capaz de identificar tokens, fazer análise sintática, e gerar código assembly correspondente.

### Requisitos 
Python 3.x instalado <br>
Verificar versão:
```
python3 --version
```
Matplotlib <br>
```
pip install matplotlib
```

### Como compilar 
Este projeto foi desenvolvido em Python, uma linguagem interpretada, portanto não há etapa de compilação explícita. <br>
A execução é feita diretamente pelo interpretador Python.<br>

### Como executar -> ATUALIZAR
Após clonar o diretório, rode o comando <br>
```
python3 AnalisadorSintatico.py nome_do_seu_arquivo.txt
```
Onde:
* `AnalisadorSintatico.py` é o arquivo principal do projeto
* `nome_do_seu_arquivo.txt` contém as expressões a serem analisadas. O arquivo deverá estar em formato txt, contendo apenas operações suportadas. Para criar seu próprio arquivo, utilize `teste01.txt` como exemplo.<br>

_Observação:_
Dependendo da configuração do sistema operacional, o comando `python` pode estar vinculado ao Python 3. Nesse caso, o comando `python3` pode ser substituído por `python`. <br>

### Como testar
#### Rodando com programas de teste fornecidos
1. Após clonar o diretório, rode o comando
```
python3 AnalisadorSintatico.py teste01.txt
```
*Também estão disponiveis os arquivos teste02.txt, teste03.txt e teste_erros_sintaticos.txt* <br>

2. O arquivo `saida.s` será gerado automaticamente, com código assembly.<br>
3. Copie seu conteúdo e cole no simulador Cpulator-ARMv7 DEC1-SOC(v16.1). <br>
4. Clique em "Compile and Load", espere a interface exibir a mensagem de "Compile succeeded" em Messages. <br>
5. OPCIONAL : Em "Settings" mude "Format" para "Decimal signed" se quiser ver as operações realizadas em tempo real.<br>
6. OPCIONAL : Use "Step Over" para ver as instruções sendo executadas passo a passo (visualize em d0 os resultados das operações).<br>
7. Clique em "Continue" e verifique na JTAG UART os resultados em hexadecimal. Verifique se os resultados estão corretos visualizando (no terminal em que o comando do passo 1 foi rodado) os valores esperados para as operações. <br>

#### Rodando funções de testes -> ATUALIZAR
```
python3 teste_analisadorLexico.py
```
_Obs : acesse os arquivos para verificação de detalhes dos testes_ <br>

### Novas estruturas
**Para a presente documentação , consideraremos :** <br>
`stmt` = qualquer instrução completa entre parênteses <br>

**Expressões com operadores relacionais**
_Neste exemplo, CONTADOR é uma variável com o valor 5 armazenado; A e B podem ser números ou `stmt`_
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (A B ==) | Verificar se o primeiro parâmetro é igual ao segundo | (10 (CONTADOR) ==) | Falso 
| (A B !=) | Verificar se o primeiro parâmetro é diferente do segundo | (10 (CONTADOR) !=) | Verdadeiro
| (A B >) | Verificar se o primeiro parâmetro é maior que o segundo | (10 (CONTADOR) >) | Verdadeiro
| (A B <) | Verificar se o primeiro parâmetro é menor que o segundo | (10 (CONTADOR) <)| Falso
| (A B >=) | Verificar se o primeiro parâmetro é maior ou igual ao segundo | (5 (CONTADOR) >=) | Verdadeiro
| (A B <=) | Verificar se o primeiro parâmetro é menor ou igual ao segundo | (5 (CONTADOR) <=) | Verdadeiro

**Estrutura de decisão**
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (stmt stmt IF) | Realizar uma comando (stmt) caso a instrução (stmt) retorne um valor diferente de 0 | ((5 5 ==) (1 2 +) IF) | Será executada o comando (1 2 +)

**Estrutura de repetição**
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (N stmt FOR) | Repete o comando (stmt) N (número inteiro positivo) vezes | (3 ((1 (CONTADOR) +) CONTADOR) FOR) | Incrementa o contador  3 vezes, com este contendo o valor 8 ao final do loop FOR


### Observações -> ATUALIZAR
1. Os arquivos de saída em assembly, tokens e árvore sintática mostrados no repositório são correspondentes ao `teste03.txt`.<br>
2. Foi usado `|` para divisão real e `/`pra divisão inteira, como especificado no documento da segunda fase.<br>-> ATUALIZAR
