# RA2-6
### Analisador Sintático
**Instituição** : PUCPR - Pontifícia Universidade Católica do Paraná<br>
**Disciplina** : Linguagens Formais e Compiladores (Turma 9º U) - Engenharia de Computação (Noite) - 2026 / 1º Sem <br>
**Professor** : Frank Coelho de Alcantara<br>
**Aluna** : Beatriz Perotto Muniz [@beatrizperottomuniz](https://github.com/beatrizperottomuniz)<br>

### Descrição
Este projeto implementa um analisador léxico capaz de identificar tokens e gerar código assembly correspondente.

### Requisitos 
Python 3.x instalado <br>
Verificar versão:
```
python3 --version
```

### Como compilar 
Este projeto foi desenvolvido em Python, uma linguagem interpretada, portanto não há etapa de compilação explícita. <br>
A execução é feita diretamente pelo interpretador Python.<br>

### Como executar
Após clonar o diretório, rode o comando <br>
```
python3 main.py nome_do_seu_arquivo.txt
```
Onde:
* `main.py` é o arquivo principal do projeto
* `nome_do_seu_arquivo.txt` contém as expressões a serem analisadas. O arquivo deverá estar em formato txt, contendo apenas operações suportadas. Para criar seu próprio arquivo, utilize `teste01.txt` como exemplo.<br>

_Observação:_
Dependendo da configuração do sistema operacional, o comando `python` pode estar vinculado ao Python 3. Nesse caso, o comando `python3` pode ser substituído por `python`. <br>

### Como testar
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

#### Rodando funções de testes
```
python3 teste_analisadorLexico.py
```
_Obs : acesse os arquivos para verificação de detalhes dos testes_ <br>

### Observações
1. O nome do diretório não aparece como RA1 6 pois a plataforma não permite, adicionando um '-' <br>
2. Foi requisitado que fosse testado com entradas com parênteses desbalanceados, este teste está incluído no arquivo de testes para processo completo, e não no de analisador léxico, pois a função responsável pela validação não está incluída neste módulo, já que essa verificação não faz parte do processo de análise léxica, que apenas gera os tokens.<br>
3. A assinatura da função `gerarAssembly(const std::vector< std::string >& _tokens_, std::string& codigoAssembly)` foi alterada para referenciar um VETOR de string "codigoAssembly" , já que na linguagem usada strings são imutáveis. <br>
4. A função executarExpressao está no main porque o enunciado exige (seção 26.7.4), e é usada para validar o Assembly gerado, como indicado na seção 26.7.2. O cálculo real ocorre no Assembly rodando no CPUlator.<br>
5. Os arquivos de saída em assembly e de tokens mostrados no repositório são correspondentes ao `teste03.txt`.<br>
