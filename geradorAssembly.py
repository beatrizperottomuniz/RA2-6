'''
Aluna : Beatriz Perotto Muniz @beatrizperottomuniz
Grupo : RA1 6
'''
import struct
from Token import TokenType
from globalVars import string_pool_global

constantes = {}        # valor -> label no assembly
variaveis = set()      # nomes das variaveis salvas
resultados_linha = []  # lbl dos resultados de cada linha para RES
contador_label = 0


def novoLabel(prefixo="LBL") -> str:
    global contador_label
    contador_label += 1
    return f"{prefixo}_{contador_label}"

def doubleParaBits(valor) -> tuple:
    #string para duas palavras de 32 b (IEEE 754 64 b little-endian)
    packed = struct.pack('<d', float(valor))
    word_baixo = struct.unpack('<I', packed[0:4])[0]
    word_alto = struct.unpack('<I', packed[4:8])[0]
    return word_baixo, word_alto

def resgatarLexema(token) -> str:
    operadores = {TokenType.PLUS: "+", TokenType.MINUS: "-", TokenType.MULT: "*", 
                  TokenType.DIV: "/", TokenType.INT_DIV: "//", TokenType.MOD: "%", TokenType.POW: "^"}
    if token.tipo in operadores:
        return operadores[token.tipo]
    if token.simbolo_id is not None:
        return string_pool_global.obterString(token.simbolo_id)
    return ""


def gerarAssembly(_tokens_: list, codigoAssembly: list) -> None:
    global contador_label
    asm = []
    
    linha_atual = len(resultados_linha) + 1
    ultimo_foi_val = False
    ultimo_foi_literal = False
    ultimo_num = "0"
    tem_eof = False

    asm.append(f"\n    @ --- linha {linha_atual} ---")

    for token in _tokens_:
        if token.tipo == TokenType.EOF:
            tem_eof = True
            continue

        if token.tipo in (TokenType.LPAREN, TokenType.RPAREN):
            continue

        lex = resgatarLexema(token)

        if token.tipo in (TokenType.NUM_INT, TokenType.NUM_FLOAT):
            lex = str(float(lex)) # para n duplicar (tipo 2.0 e 2)
            
            if lex not in constantes:
                constantes[lex] = novoLabel("CONST")
            
            lbl = constantes[lex]
            
            asm.append(f"    LDR r0, ={lbl}")
            asm.append(f"    VLDR d0, [r0]")
            asm.append(f"    VSTMDB sp!, {{d0}}")
            
            ultimo_foi_val = True
            ultimo_foi_literal = True
            ultimo_num = lex

        elif token.tipo == TokenType.ID:
            variaveis.add(lex)
            if ultimo_foi_literal:
                # Store
                asm.append(f"    VLDMIA sp!, {{d0}}")
                asm.append(f"    LDR r1, ={lex}_MEM")
                asm.append(f"    VSTR d0, [r1]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
            else:
                # Load -> carrega p/ pilha)
                asm.append(f"    LDR r0, ={lex}_MEM")
                asm.append(f"    VLDR d0, [r0]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
            ultimo_foi_val = True
            ultimo_foi_literal = False

        elif token.tipo == TokenType.KEYWORD_RES:
            #n = int(ultimo_num)
            n = int(float(ultimo_num))
            asm.append(f"    ADD sp, sp, #8")

            indice = (linha_atual - 1) - n

            # n=0 ou indice invalido: retorna 0.0
            if n == 0 or indice < 0 or indice >= len(resultados_linha):
                if "0.0" not in constantes:
                    constantes["0.0"] = novoLabel("CONST")
                asm.append(f"    LDR r0, ={constantes['0.0']}")
                asm.append(f"    VLDR d0, [r0]")
                asm.append(f"    VSTMDB sp!, {{d0}}")
                ultimo_foi_val = True
                ultimo_foi_literal = False
                continue

            lbl_res = resultados_linha[indice]
            asm.append(f"    LDR r0, ={lbl_res}")
            asm.append(f"    VLDR d0, [r0]")
            asm.append(f"    VSTMDB sp!, {{d0}}")
            ultimo_foi_val = True
            ultimo_foi_literal = False

        elif token.tipo in (TokenType.PLUS, TokenType.MINUS, TokenType.MULT, TokenType.DIV, 
                            TokenType.INT_DIV, TokenType.MOD, TokenType.POW):
            
            # desempilhar operandos (d1 = direita, d0 = esquerda)
            asm.append(f"    VLDMIA sp!, {{d1}}")
            asm.append(f"    VLDMIA sp!, {{d0}}")

            if token.tipo == TokenType.PLUS:
                asm.append("    VADD.F64 d0, d0, d1")
            elif token.tipo == TokenType.MINUS:
                asm.append("    VSUB.F64 d0, d0, d1")
            elif token.tipo == TokenType.MULT:
                asm.append("    VMUL.F64 d0, d0, d1")
            elif token.tipo == TokenType.DIV:
                asm.append("    VDIV.F64 d0, d0, d1")
                
            elif token.tipo == TokenType.INT_DIV:
                asm.append("    VDIV.F64 d2, d0, d1")
                asm.append("    VCVT.S32.F64 s4, d2")
                asm.append("    VCVT.F64.S32 d0, s4")
                
            elif token.tipo == TokenType.MOD:
                asm.append("    VDIV.F64 d2, d0, d1")
                asm.append("    VCVT.S32.F64 s4, d2")
                asm.append("    VCVT.F64.S32 d2, s4")
                asm.append("    VMUL.F64 d2, d2, d1")
                asm.append("    VSUB.F64 d0, d0, d2")
                
            elif token.tipo == TokenType.POW:
                lbl_loop = novoLabel("POW_LOOP")
                lbl_fim  = novoLabel("POW_FIM")
                
                asm.append("    VMOV.F64 d2, d0")
                asm.append("    VCVT.S32.F64 s0, d1")
                asm.append("    VMOV r2, s0")
                
                if "1.0" not in constantes: constantes["1.0"] = novoLabel("CONST")
                asm.append(f"    LDR r0, ={constantes['1.0']}")
                asm.append("    VLDR d0, [r0]")
                
                asm.append(f"{lbl_loop}:")
                asm.append("    CMP r2, #0")
                asm.append(f"    BLE {lbl_fim}")
                asm.append("    VMUL.F64 d0, d0, d2")
                asm.append("    SUB r2, r2, #1")
                asm.append(f"    B {lbl_loop}")
                asm.append(f"{lbl_fim}:")

            asm.append("    VSTMDB sp!, {d0}")
            ultimo_foi_val = True
            ultimo_foi_literal = False

    lbl_linha = f"RES_LINHA_{linha_atual}"
    resultados_linha.append(lbl_linha)
    
    if ultimo_foi_val:
        asm.append(f"    VLDMIA sp!, {{d0}}")
        asm.append(f"    LDR r3, ={lbl_linha}")
        asm.append(f"    VSTR d0, [r3]")
        asm.append(f"    LDR r0, ={lbl_linha}")
        asm.append(f"    BL PRINT_RES_HEX")

    codigoAssembly.extend(asm)
    if tem_eof:
        finalizarAssembly(codigoAssembly)



def finalizarAssembly(codigo: list) -> None:
    out = [
        "    .syntax unified",
        "    .arch armv7-a",
        "    .fpu vfpv3-d16",
        "",
        "    .data"
    ]

    # vars 8 bytes
    for v in variaveis:
        out.append(f"{v}_MEM: .space 8")
    for res in resultados_linha:
        out.append(f"{res}: .space 8")

    # consts
    for val, lbl in constantes.items():
        wb, wa = doubleParaBits(val)
        out.append(f"{lbl}: .word 0x{wb:08X}, 0x{wa:08X} @ valor: {val}")

    out.extend([
        "",
        "    .text",
        """                                             
  @ UART_PUTCHAR - envia r0 (1 byte) por UART                                          
  UART_PUTCHAR:                                                                                     
      PUSH {r1, r2, lr}                                                                             
      LDR r2, =0xFF201000                                                                           
  _UART_WAIT:                                                                                     
      LDR r1, [r2, #4]        
      LSR r1, r1, #16                                                 
      CMP r1, #0                                                                                    
      BEQ _UART_WAIT                                                           
      STRB r0, [r2]                                                                 
      POP {r1, r2, pc}                                                                              
                                                                                                      
  @ PRINT_NIBBLES_32 - imprime r7 como 8 digitos hex
  PRINT_NIBBLES_32:                                                                                 
      PUSH {r6, r7, lr}                                                                             
      MOV r6, #8                                                   
  _LOOP_NIB:                                                                                        
      MOV r0, r7, LSR #28     
      AND r0, r0, #0xF                                                                              
      CMP r0, #10                                                                                 
      ADDLT r0, r0, #48       @ 0–9 :'0' = 48                                                    
      ADDGE r0, r0, #55       @ A–F :'A'–10 = 55                                                 
      BL UART_PUTCHAR
      LSL r7, r7, #4                                                             
      SUBS r6, r6, #1                                                                             
      BNE _LOOP_NIB                                                                                 
      POP {r6, r7, pc}                                                                            
                                                                                                                                                                                                      
  @ PRINT_RES_HEX - imprime double de 64 bits em hex
  @ r0 = endereco do valor                                                   
  PRINT_RES_HEX:                                                                                    
      PUSH {r4, r5, lr}                                                                             
      LDR r4, [r0]            @ word baixo                             
      LDR r5, [r0, #4]        @ word alto                                         
                                                                                                    
      MOV r0, #48             @ '0'                                                                 
      BL UART_PUTCHAR                                                                               
      MOV r0, #120            @ 'x'                                                               
      BL UART_PUTCHAR
                                                                                                    
      MOV r7, r5              @ word alto primeiro 
      BL PRINT_NIBBLES_32                                                                           
      MOV r7, r4              @ word baixo                                               
      BL PRINT_NIBBLES_32                                                                           
  
      MOV r0, #13             @ r                                                                
      BL UART_PUTCHAR                                                                             
      MOV r0, #10             @ n 
      BL UART_PUTCHAR                                                                               
  
      POP {r4, r5, pc}                                                                              
                        """,
        "    .global _start",
        "_start:",
        "    MRC p15, 0, r1, c1, c0, 2",
        "    ORR r1, r1, #(0xF << 20)",
        "    MCR p15, 0, r1, c1, c0, 2",
        "    MOV r1, #0x40000000",
        "    FMXR FPEXC, r1"
    ])

    out.extend(codigo)

    out.extend([
        "",
        "_end:",
        "    B _end"
    ])

    # return "\n".join(out)

    # assembly_final = finalizarAssembly(linhas_assembly)
    # with open("saida.s", "w") as f:
    #     f.write(assembly_final)

    texto_final = "\n".join(out)
    with open("saida.s", "w") as f:
        f.write(texto_final)