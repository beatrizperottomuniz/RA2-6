# Gramática 

## Regras de produção
```
prog → LPAREN KEYWORD_START RPAREN list_stmts EOF

list_stmts → LPAREN list_item

list_item  → KEYWORD_END RPAREN
list_item  → rpn RPAREN list_stmts

stmt → LPAREN rpn RPAREN

rpn → num   rpn_tail_num
rpn → stmt  rpn_tail_stmt
rpn → ID

num      → NUM_INT
num      → NUM_FLOAT
num      → MINUS num_tipo
num_tipo → NUM_INT
num_tipo → NUM_FLOAT

rpn_tail_num  → KEYWORD_RES
rpn_tail_num  → ID
rpn_tail_num  → num  op_bin
rpn_tail_num  → stmt op_stmt_num

rpn_tail_stmt → ID
rpn_tail_stmt → num  op_bin
rpn_tail_stmt → stmt op_stmt_stmt

op_stmt_num  → KEYWORD_FOR | op_arit | op_rel
op_stmt_stmt → KEYWORD_IF | KEYWORD_ELSE | op_arit | op_rel
op_bin  → op_arit | op_rel

op_arit → PLUS | MINUS | MULT | DIV | INT_DIV | MOD | POW
op_rel  → GT | LT | GTE | LTE | EQ | NEQ
```

## Terminais
KEYWORD_RES = "KEYWORD_RES"
KEYWORD_START = "KEYWORD_START"
KEYWORD_END = "KEYWORD_END"
KEYWORD_IF = "KEYWORD_IF"
KEYWORD_ELSE = "KEYWORD_ELSE" 
KEYWORD_FOR = "KEYWORD_FOR"
ID = "ID"
NUM_INT = "NUM_INT"
NUM_FLOAT = "NUM_FLOAT"
PLUS = "PLUS"
MINUS = "MINUS"
MULT = "MULT"
DIV = "DIV"
INT_DIV = "INT_DIV"
MOD = "MOD"
POW = "POW"
GT  = "GT"  # >
LT  = "LT"  # <
GTE = "GTE"  # >=
LTE = "LTE"  # <=
EQ  = "EQ"  # ==
NEQ = "NEQ"  # !=
LPAREN = "LPAREN"
RPAREN = "RPAREN"
EOF = "EOF"

_Obs: Como pedido no tópico 27.7.1 : "Documentar a gramática completa em formato EBNF (use letras minúsculas para não-terminais e maiúsculas para terminais)."_