'''
Integrantes do grupo:
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