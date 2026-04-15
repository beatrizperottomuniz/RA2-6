'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
from Token import Token, TokenType
from stringPool import StringPool
import globalVars

class Lexer:
    def __init__(self, src: str, string_pool: StringPool,linha_count: int):
        self.src = src
        self.string_pool = string_pool
        self.pos = 0
        self.linha = linha_count
        self.col = 1
        self.buffer = []
        self.tokens = []

        self.inicio_col = 1
        self.estado_atual = self.estadoInicio
        self.keywords = {"RES": TokenType.KEYWORD_RES}
        self.operadores = "+-*/%^"
        self.simbolos = {
            '+': TokenType.PLUS,
            '-': TokenType.MINUS,
            '*': TokenType.MULT,
            '/': TokenType.DIV,
            '%': TokenType.MOD,
            '^': TokenType.POW,
        }

    # olha proximo sem consumir
    def peek(self): 
        return self.src[self.pos] if self.pos < len(self.src) else None

    def advance(self):
        char = self.peek()
        if char is not None:
            self.pos += 1
            self.col += 1
        return char

    # salva token e limpa buffer
    def emit(self, token_type: str):
        lex_str = "".join(self.buffer)
        simbolo_id = 0

        if token_type == TokenType.ID:
            if lex_str in self.keywords:
                token_type = self.keywords[lex_str]
            else:
                simbolo_id = self.string_pool.buscarOuAdicionar(lex_str)
        elif token_type in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
            simbolo_id = self.string_pool.buscarOuAdicionar(lex_str)
            
        elif token_type == TokenType.UNKNOWN:
            str_erro = lex_str 
            print(f"Erro na linha {self.linha}, coluna {self.inicio_col}: {str_erro}\n")

        self.tokens.append(Token(token_type, self.linha, self.inicio_col, simbolo_id))
        self.buffer.clear()


    def tokenize(self):
        while self.estado_atual is not None:
            self.estado_atual = self.estado_atual()
        return self.tokens

    # funcoes de estados ------------------------------------

    # estado inicial
    def estadoInicio(self):
        char = self.peek()

        if char is None:
            if self.linha == globalVars.total_linhas_global:
                self.tokens.append(Token(TokenType.EOF, self.linha, self.col,0))
            return None

        if char.isspace():
            self.advance()
            return self.estadoInicio

        self.inicio_col = self.col

        # transicao estado de id -> apenas conjunto de letras maiusculas
        if char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.estadoId

        # transicao estado de num_int
        if char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.estadoNumInt

        # transicao estado de operadores
        if char in self.operadores:
            self.buffer.append(char)
            self.advance()
            return self.estadoOperador

        # transicao estado de parenteses
        if char in "()":
            self.buffer.append(char)
            self.advance()
            return self.estadoParen

        self.buffer.append(char)
        self.advance()
        self.emit(TokenType.UNKNOWN)
        return self.estadoInicio


    def estadoOperador(self):
        char = self.buffer[0]
        if char == '/' and self.peek() == '/':
            self.buffer.append(self.peek())
            self.advance()
            self.emit(TokenType.INT_DIV)
            return self.estadoInicio

        if char in self.simbolos:
            self.emit(self.simbolos[char])
        else:
            self.emit(TokenType.UNKNOWN)
            
        return self.estadoInicio


    def estadoParen(self):
        char = self.buffer[0]
        if char == '(':
            self.emit(TokenType.LPAREN)
        elif char == ')':
            self.emit(TokenType.RPAREN)
            
        return self.estadoInicio
    

    def estadoId(self):
        char = self.peek()
        if char is not None and char.isalpha() and char.isupper():
            self.buffer.append(char)
            self.advance()
            return self.estadoId
            
        self.emit(TokenType.ID)
        return self.estadoInicio


    def estadoNumInt(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.estadoNumInt
            
        if char == '.':
            self.buffer.append(char)
            self.advance()
            return self.estadoNumFloat
            
        self.emit(TokenType.NUM_INT)
        return self.estadoInicio


    def estadoNumFloat(self):
        char = self.peek()
        if char is not None and char.isdigit():
            self.buffer.append(char)
            self.advance()
            return self.estadoNumFloat
            
        if char == '.':
            # estado de erro para + de um ponto
            self.buffer.append(char)
            self.advance()
            return self.estadoNumInvalido
            
        self.emit(TokenType.NUM_FLOAT)
        return self.estadoInicio


    # estado de erro para consumir o resto do numero float errado -> ex : 1.2.34
    def estadoNumInvalido(self):
        char = self.peek()
        if char is not None and (char.isdigit() or char == '.'):
            self.buffer.append(char)
            self.advance()
            return self.estadoNumInvalido
            
        self.emit(TokenType.UNKNOWN)
        return self.estadoInicio


# _tokens_ vem por referencia
def parseExpressao(linha: str, _tokens_ : list) -> None:
    lexer = Lexer(linha, globalVars.string_pool_global, globalVars.contador_linha_global)
    #return lexer.tokenize()
    tokens = lexer.tokenize()
    _tokens_.extend(tokens)
