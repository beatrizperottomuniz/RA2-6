# RA2-6
### Analisador Sintático
**Instituição** : PUCPR - Pontifícia Universidade Católica do Paraná<br>
**Disciplina** : Linguagens Formais e Compiladores (Turma 9º U) - Engenharia de Computação (Noite) - 2026 / 1º Sem <br>
**Professor** : Frank Coelho de Alcantara<br>
**Aluna** : Beatriz Perotto Muniz [@beatrizperottomuniz](https://github.com/beatrizperottomuniz)<br>

### Descrição -> ATUALIZAR
Este projeto implementa um analisador léxico capaz de identificar tokens e gerar código assembly correspondente.

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
python3 main.py nome_do_seu_arquivo.txt
```
Onde:
* `main.py` é o arquivo principal do projeto
* `nome_do_seu_arquivo.txt` contém as expressões a serem analisadas. O arquivo deverá estar em formato txt, contendo apenas operações suportadas. Para criar seu próprio arquivo, utilize `teste01.txt` como exemplo.<br>

_Observação:_
Dependendo da configuração do sistema operacional, o comando `python` pode estar vinculado ao Python 3. Nesse caso, o comando `python3` pode ser substituído por `python`. <br>

### Como testar -> ATUALIZAR
#### Rodando com programas de teste fornecidos
1. Após clonar o diretório, rode o comando
```
python3 main.py teste01.txt
```
_Obs : também estão disponiveis os arquivos teste02.txt e teste03.txt_ <br>

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

### Novas estruturas -> ATUALIZAR
**Para a presente documentação , consideraremos :** <br>
`exp` = um número inteiro (ex: 20); um número real (ex: 20.1); uma leitura de memória (ex: (X)); um resultado anterior lido com RES (ex: (1 RES)); uma expressão aritmética aninhada. A única operacao definida na fase anterior que nao pode ser usada é a atribuicao de um valor a memoria (ex: (1 CONTADOR)) <br>
`stmt` = qualquer instrução completa entre parênteses <br>
`cond` = expressão que retorna verdadeiro ou falso: (`exp exp operador_relacional`) <br>
`operador_relacional` = `==`, `!=`, `>`, `<`, `>=`, `<=` <br>

**Expressões de condição (cond)**
_Neste exemplo, CONTADOR é uma variável com o valor 5 armazenado_
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (exp exp ==) | Verificar se o primeiro parâmetro é igual ao segundo | (10 (CONTADOR) ==) | Falso 
| (exp exp !=) | Verificar se o primeiro parâmetro é diferente do segundo | (10 (CONTADOR) !=) | Verdadeiro
| (exp exp >) | Verificar se o primeiro parâmetro é maior que o segundo | (10 (CONTADOR) >) | Verdadeiro
| (exp exp <) | Verificar se o primeiro parâmetro é menos que o segundo | (10 (CONTADOR) <)| Falso
| (exp exp >=) | Verificar se o primeiro parâmetro é maior ou igual ao segundo | (5 (CONTADOR) >=) | Verdadeiro
| (exp exp <=) | Verificar se o primeiro parâmetro é menor ou igual ao segundo | (5 (CONTADOR) <=) | Verdadeiro

**Estrutura de decisão**
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (cond stmt IF) | Realizar uma comando (stmt) caso a condição (cond) seja satisfeita | ((5 5 ==) (1 2 +) IF) | Será executada o comando (1 2 +)

**Laços de controle**
| Comando | Função | Exemplo | Resultado esperado para o exemplo |
|----------|----------|----------|----------|
| (N stmt FOR) | Repete o comando (stmt) N (número inteiro positivo maior que 1) vezes (passo 1, de 1 até N)| (3 ((1 (CONTADOR) +) CONTADOR) FOR) | Incrementa o contador  3 vezes, com este contendo o valor 8 ao final do loop FOR


### Observações -> ATUALIZAR
1. Foi requisitado que fosse testado com entradas com parênteses desbalanceados, este teste está incluído no arquivo de testes para processo completo, e não no de analisador léxico, pois a função responsável pela validação não está incluída neste módulo, já que essa verificação não faz parte do processo de análise léxica, que apenas gera os tokens.<br>
2. Os arquivos de saída em assembly e de tokens mostrados no repositório são correspondentes ao `teste03.txt`.<br>
3. Foi usado `/` para divisão real e `//`pra divisão inteira, como especificado na primeira fase, após professor confirmar que o enunciado teve erro de digitação.<br>
