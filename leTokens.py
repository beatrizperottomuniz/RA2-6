'''
Integrantes do grupo (ordem alfabética):
Beatriz Perotto Muniz - @beatrizperottomuniz

Nome do grupo no Canvas: RA2 6
'''
import json
from globalVars import string_pool_global
from Token import Token

def lerTokens(arquivo ="saida_tokens.txt") -> list:
    try:
        with open(arquivo, 'r', encoding='utf-8') as file:
            dados = json.load(file)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {arquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")

    # coloca dados na string pool
    for lexema in dados["string_pool"]:
        string_pool_global.buscarOuAdicionar(lexema)

    # faz a lista de tokens
    lista_tokens = []
    for t in dados["tokens"]:
        token = Token(t["tipo"], t["linha"], t["coluna"], t["simbolo_id"])
        lista_tokens.append(token)

    return lista_tokens


# # validação básica de estrutura                                                               
# if "string_pool" not in dados or "tokens" not in dados:
#     print(f"Formato inválido: campos 'string_pool' ou 'tokens' ausentes.")                      
#     return []                                                                                   
                                                                                                
# tipos_validos = {t for t in dir(TokenType) if not t.startswith('_')}                            
# for i, t in enumerate(dados["tokens"]):                                                       
#     if not all(k in t for k in ("tipo", "linha", "coluna", "simbolo_id")):                      
#         print(f"Token {i} com campos faltando: {t}")                                            
#         return []                                                                               
#     if t["tipo"] not in tipos_validos:                                                          
#         print(f"Tipo de token desconhecido na posição {i}: '{t['tipo']}'")                      
#         return []                                                                               

# tipos = [t["tipo"] for t in dados["tokens"]]                                                    
# if "EOF" not in tipos:                                                                        
#     print("Arquivo de tokens sem EOF — pode estar corrompido.")                                 
#     return [] 