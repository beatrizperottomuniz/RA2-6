'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
class TokenType:
    # keyword
    KEYWORD_RES = "KEYWORD_RES"
    # id (variaveis) e tipos literais
    ID = "ID"
    NUM_INT = "NUM_INT"
    NUM_FLOAT = "NUM_FLOAT"
    # operadores
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULT = "MULT"
    DIV = "DIV"
    INT_DIV = "INT_DIV"
    MOD = "MOD"
    POW = "POW"
    # divisor de operacoes
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    # outros
    EOF = "EOF"
    UNKNOWN = "UNKNOWN"

# classe do token com tipo,linha, coluna, id do simbolo na string pool
class Token:
    def __init__(self, token_tipo: str, linha: int, coluna: int, simbolo_id : int):
        self.tipo = token_tipo
        self.linha = linha
        self.coluna = coluna
        self.simbolo_id = simbolo_id

    def __repr__(self):
        return f"Token({self.tipo}, {self.simbolo_id}, {self.linha}, {self.coluna})"

