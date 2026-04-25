'''
Integrantes do grupo (ordem alfabética):
Beatriz Perotto Muniz - @beatrizperottomuniz

Nome do grupo no Canvas: RA2 6
'''
def lerArquivo(nomeArquivo: str, linhas: list) -> None:
    try:
        with open(nomeArquivo, encoding='utf-8') as arquivo:
            for linha in arquivo:
                linhas.append(linha.rstrip('\n'))
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nomeArquivo}")
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
