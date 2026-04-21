'''
Integrantes do grupo:
Beatriz Perotto Muniz - @beatrizperottomuniz

Nome do grupo no Canvas: RA2 6
'''
# terminais = TokenType (ex: "PLUS")

gramatica_definida = {
    'prog': [
        ['LPAREN', 'KEYWORD_START', 'RPAREN', 'list_stmts', 'EOF']
    ],
    'list_stmts': [
        ['LPAREN', 'list_item']
    ],
    'list_item': [
        ['KEYWORD_END', 'RPAREN'],
        ['rpn', 'RPAREN', 'list_stmts']
    ],
    'stmt': [
        ['LPAREN', 'rpn', 'RPAREN']
    ],
    'rpn': [
        ['num',  'rpn_tail_num'],
        ['stmt', 'rpn_tail_stmt'],
        ['ID']
    ],
    'num': [
        ['NUM_INT'],
        ['NUM_FLOAT'],
        ['MINUS', 'num_tipo']
    ],
    'num_tipo': [
        ['NUM_INT'],
        ['NUM_FLOAT']
    ],
    'rpn_tail_num': [
        ['KEYWORD_RES'],
        ['ID'],
        ['num',  'op_bin'],
        ['stmt', 'op_stmt_num']
    ],
    'rpn_tail_stmt': [
        ['ID'],
        ['num',  'op_bin'],
        ['stmt', 'op_stmt_stmt']
    ],
    'op_stmt_num': [
        ['KEYWORD_FOR'],
        ['op_arit'],
        ['op_rel']
    ],
    'op_stmt_stmt': [
        ['KEYWORD_IF'],
        ['KEYWORD_ELSE'],
        ['op_arit'],
        ['op_rel']
    ],
    'op_bin': [
        ['op_arit'],
        ['op_rel']
    ],
    'op_arit': [
        ['PLUS'],
        ['MINUS'],
        ['MULT'],
        ['DIV'],
        ['INT_DIV'],
        ['MOD'],
        ['POW']
    ],
    'op_rel': [
        ['GT'],
        ['LT'],
        ['GTE'],
        ['LTE'],
        ['EQ'],
        ['NEQ']
    ]
}

simbolo_inicial_gramatica = 'prog'
epsilon = 'ε'

# auxiliares

# A logica de calculo das funcoes foi adaptada a partir do pseudocodigo de: https://frankalcantara.com/lf/05-parsersLL1.html
# nas regras atuais nenhum nt é nullable, feito pra proximas fases se precisar
def calcularNullable(gramatica):
    nullable = set()
    for nt, producoes in gramatica.items():
        for producao in producoes:
            if not producao or producao == [epsilon]:
                nullable.add(nt)
    mudou = True
    while mudou:
        mudou = False
        for nt, producoes in gramatica.items():
            if nt not in nullable:
                for producao in producoes:
                    if not producao or producao == [epsilon]:
                        continue
                    
                    todos_sao_nullable = all((simbolo in nullable) for simbolo in producao)
                    if todos_sao_nullable:
                        nullable.add(nt)
                        mudou = True
                        break 
    return nullable


def eTerminal(simbolo, gramatica):
    return simbolo not in gramatica


def firstDeSequencia(sequencia, first, gramatica, nullable):
   # calcula FIRST de uma sequencia de simbolos
    resultado = set()
    for simbolo in sequencia:
        if eTerminal(simbolo, gramatica):
            if simbolo != epsilon:
                resultado.add(simbolo)
            break
        else:
            resultado.update(first[simbolo] - {epsilon})
            if simbolo not in nullable:
                break
    else:
        resultado.add(epsilon)
    return resultado


def calcularFirst(gramatica, nullable):
    # só pros nts, o de um terminal é ele mesmo
    firsts = {nt: set() for nt in gramatica}

    mudou = True
    while mudou:
        mudou = False
        for nt, producoes in gramatica.items():
            for producao in producoes:
                antes = len(firsts[nt])
                firsts[nt].update(firstDeSequencia(producao, firsts, gramatica, nullable))
                if len(firsts[nt]) != antes:
                    mudou = True

    return firsts


def calcularFollow(gramatica, first, nullable, simbolo_inicial=simbolo_inicial_gramatica):
    follow = {nt: set() for nt in gramatica}
    follow[simbolo_inicial].add('EOF')

    mudou = True
    while mudou:
        mudou = False
        for nt, producoes in gramatica.items():
            for producao in producoes:
                for i, simbolo in enumerate(producao):
                    if not eTerminal(simbolo, gramatica):
                        beta = producao[i + 1:]
                        first_beta = firstDeSequencia(beta, first, gramatica, nullable)

                        antes = len(follow[simbolo])
                        follow[simbolo].update(first_beta - {epsilon})
                        if epsilon in first_beta:
                            follow[simbolo].update(follow[nt])
                        if len(follow[simbolo]) != antes:
                            mudou = True

    return follow


def construirTabelaLL1(gramatica, first, follow, nullable):
    tabela = {nt: {} for nt in gramatica}
    conflitos = []

    for nt, producoes in gramatica.items():
        for producao in producoes:
            first_prod = firstDeSequencia(producao, first, gramatica, nullable)
            terminais = first_prod - {epsilon}

            if epsilon in first_prod:
                terminais.update(follow[nt])

            for terminal in terminais:
                if terminal in tabela[nt]:
                    conflitos.append((nt, terminal))
                else:
                    tabela[nt][terminal] = producao

    if conflitos:
        for nt, terminal in conflitos:
            print(f"[CONFLITO LL(1)] [{nt}, {terminal}]")

    return tabela

def imprimeTabelaMarkdown(tabela: dict) -> str: # pra documentacao
    nao_terminais = sorted(tabela.keys())
    terminais_set = set()
    for nt in tabela:
        terminais_set.update(tabela[nt].keys())
    terminais = sorted(list(terminais_set))
    
    linhas_md = []
    
    cabecalho = "| Não-terminal | " + " | ".join(terminais) + " |"
    linhas_md.append(cabecalho)
    divisor = "|---|" + "|".join(["---" for _ in terminais]) + "|"
    linhas_md.append(divisor)
    
    for nt in nao_terminais:
        linha = f"| **{nt}** |"
        for t in terminais:
            producao = tabela[nt].get(t, None)
            
            if producao is None:
                linha += " |"  
            else:
                if not producao or producao == ['ε']:
                    prod_str = 'ε'
                else:
                    prod_str = " ".join(producao)
                
                linha += f" {nt} → {prod_str} |"
        linhas_md.append(linha)
        
    return "\n".join(linhas_md)


def construirGramatica():
    nullable = calcularNullable(gramatica_definida)
    gramatica = gramatica_definida
    first     = calcularFirst(gramatica, nullable)
    follow    = calcularFollow(gramatica, first, nullable)
    tabela    = construirTabelaLL1(gramatica, first, follow, nullable)

    return {
        'gramatica': gramatica,
        'nullable':  nullable,
        'first':     first,
        'follow':    follow,
        'tabela':    tabela
    }


# debug

if __name__ == '__main__':
    resultado = construirGramatica()

    print("FIRST --------------")
    for nt, conj in sorted(resultado['first'].items()):
        print(f"  FIRST({nt}) = {sorted(conj)}")

    print("\nFOLLOW --------------")
    for nt, conj in sorted(resultado['follow'].items()):
        print(f"  FOLLOW({nt}) = {sorted(conj)}")

    print("\nTABELA LL(1) --------------")
    for nt, entradas in sorted(resultado['tabela'].items()):
        for terminal, producao in sorted(entradas.items()):
            prod_str = ' '.join(producao) if producao else 'ε'
            print(f"  [{nt}, {terminal}] → {prod_str}")

    print("\nTABELA FINAL --------------")
    print(imprimeTabelaMarkdown(resultado['tabela']))
