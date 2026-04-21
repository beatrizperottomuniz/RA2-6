# Gramática 

## Regras de produção
```
prog ::= LPAREN KEYWORD_START RPAREN list_stmts EOF

list_stmts ::= LPAREN list_item

list_item  ::= KEYWORD_END RPAREN
list_item  ::= rpn RPAREN list_stmts

stmt ::= LPAREN rpn RPAREN

rpn ::= num   rpn_tail_num
rpn ::= stmt  rpn_tail_stmt
rpn ::= ID

num      ::= NUM_INT
num      ::= NUM_FLOAT
num      ::= MINUS num_tipo
num_tipo ::= NUM_INT
num_tipo ::= NUM_FLOAT

rpn_tail_num  ::= KEYWORD_RES
rpn_tail_num  ::= ID
rpn_tail_num  ::= num  op_bin
rpn_tail_num  ::= stmt op_stmt_num

rpn_tail_stmt ::= ID
rpn_tail_stmt ::= num  op_bin
rpn_tail_stmt ::= stmt op_stmt_stmt

op_stmt_num  ::= KEYWORD_FOR | op_arit | op_rel
op_stmt_stmt ::= KEYWORD_IF | KEYWORD_ELSE | op_arit | op_rel
op_bin  ::= op_arit | op_rel

op_arit ::= PLUS | MINUS | MULT | DIV | INT_DIV | MOD | POW
op_rel  ::= GT | LT | GTE | LTE | EQ | NEQ
```

## Terminais
```
KEYWORD_RES = RES
KEYWORD_START = START
KEYWORD_END = END
KEYWORD_IF = IF
KEYWORD_ELSE = ELSE
KEYWORD_FOR = FOR

ID = variáveis em letra maíuscula como X, CONTADOR
NUM_INT = números inteiros como 10
NUM_FLOAT = números reais como 10.5

PLUS = +
MINUS = -
MULT = *
DIV = /
INT_DIV = //
MOD = %
POW = ^

GT  = >
LT  = <
GTE = >=
LTE = <=
EQ  = ==
NEQ = !=

LPAREN = (
RPAREN = )

EOF = sinaliza o fim do arquivo
```

_Obs: Feita como pedido no tópico 27.7.1 : "Documentar a gramática completa em formato EBNF (use letras minúsculas para não-terminais e maiúsculas para terminais)."_