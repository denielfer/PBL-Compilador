# Conjunto de palavras reservadas
PRE =  ["variables", "const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for", "read", "print", "void", "int", "real","boolean", "string", "true", "false"]

from string import ascii_letters, digits, printable
from re import search

# Conjunto de operadores aritméticos
op_ar = ["+", "-", "*", '/', "++", "--"]

# Conjunto de operadores relacionais
op_re = '!= == < <= > >= ='.split()

# Conjunto de operadores lógicos
op_log = '! && ||'.split()

# MUDAR PARA cadeia
coment_cadeia = '"'
coment_block = ['/*']
coment_linha = ['//']

IDE_CHAR = ascii_letters + '_' + digits 
digits_p = digits + '.'

# Códigos de tokens
CODIGOS = {
    1: 'PRE',
    2: 'IDE',
    3: 'CAC',
    4: 'NRO',
    5: 'DEL',
    6: 'REL',
    7: 'LOG',
    8: 'ART',
    9: 'CMF',
    10: 'CoMF',
    11: 'NMF',
    12: 'IMF',
    13: 'TMF'
}

# SEPARADORES = op_ar + op_re + op_log + coment_cadeia + coment_block + coment_linha
SEPARADORES = { # separadores e respectivos códigos de token
    '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
    '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
    '!': 7, '&&': 7, '||': 7, 
    ';': 5, ',': 5, '.': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
    '"': 3
}

# SEPARADORES de número não contém o ponto(.)
SEPARADORES_NUMERO = {
    '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
    '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
    '!': 7, '&&': 7, '||': 7, 
    ';': 5, ',': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
    '"': 3
}

class comentario_bloco_excption(Exception):
    pass

def get_tokens(text):
    '''
        Analisa uma linha de lexemas para gerar respectivos tokens
    '''
    text += '\n' # para não quebrar o text[n+1]
    token = ''
    controle = -1 # estado atual
    erro_ponto = None
    force_continue = False
    char = None

    # Percorre os caracteres até o final da linha
    for n, char in enumerate(text[:-1]):
        print(f' {n}\t| Controle: {controle}\t|Token: {token}\t|Char Analizado: "{char}"\t|erro_ponto: {erro_ponto}\t|force_continue: {force_continue}')
    
        # Pula o caracter
        if (force_continue):
            force_continue = False
            continue
        
        # Analisa se o token é um CAC ou CMF
        elif (controle in [3, 9]):
            if (char == '"'):
                yield (controle, token + '"')
                token = ''
                controle = -1
                continue
            elif (char not in printable):
                controle = 9
            token += char

        # Procura o final do comentário de bloco
        elif (controle == 14): # comentário bloco
            if (char + text[n+1] == '*/'):
                force_continue = True
                token = ''
                controle = -1
            else:
                token += char

        # Percorre o comentário de linha até o final
        elif (controle == 15): # comentário linha
            return
        
        # Identifica um comentário de linha
        elif (char + text[n+1] == '//'):
            return
        
        # Identifica um comentário de bloco
        elif (char + text[n+1] == '/*'):
            for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
                yield token_gerado
            erro_ponto = None
            controle = 14
            force_continue = True
            token = '/*'

        # Gera o token com o estado atual quando encontra um espaço em branco
        elif (search(r'\s', char)):
            for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
                yield token_gerado
            erro_ponto = None # reseta erro de ponto de número, pois, caso for, terá valor
            token = ''
            controle = -1

        # Continua a iteração para procurar o tipo de token que será avaliado
        elif (controle == -1):
            controle = __get_controle__(char, text[n+1]) # não precisa do force continue para 14, pois esse acabou de ser verificado acima
            if (controle != -1):
                token += char

        # Analisa se o token é um IDE ou IMF
        elif (controle in [2, 12]):
            if (char in IDE_CHAR): # se ainda é char válido em indentificador
                token += char
                continue
            sep = __get_if_sep__(char, text[n+1], default_not_in = 12)
            if (sep[1] != 12): # se não for char inválido, é separador 
                yield (1 if token in PRE else controle, token)  # geramos IDE ou PRE
                token = '' # limpamos o token que está sendo gerado
            token += char
            controle = sep[1]

        # Analisa se o token é um NRO ou NMF
        elif (controle in [4, 11]):
            if (char in digits_p):
                if (erro_ponto == False):
                    erro_ponto = True
                token += char
                if (char == '.' and controle == 4):
                    if (erro_ponto is None):
                        erro_ponto = False
                    else:
                        controle = 11
                continue
            elif (erro_ponto == False): # precisa especificar se é false, pois (not erro_ponto) lança None
                # consome o token logo apos o '.' se não estiver em digitos
                token += char
                erro_ponto = True
                controle = 11
                continue
            sep = __get_if_sep__(char, text[n+1], separadores = SEPARADORES_NUMERO, default_not_in = 11)
            if (sep[1] != 11): # 11 seria nao achar separador, então entra no if se achar separador
                yield (controle, token)
                token = ''
                erro_ponto = None
            token += char
            controle = sep[1]

        # Analisa se o token é um DEL, REL, LOG ou ART
        elif (4 < controle < 9): # separadores e delimitadores
            sep = __get_if_sep__(token, char, separadores = SEPARADORES, default_not_in = -1)
            if (sep[1] != -1):
                yield (sep[1], sep[0])
                if (len(sep[0]) == 1): # se achou separador de 2 chars então já emitiu para esse char, senão, precisamos descobrir o que ele é
                    token = char
                    controle = __get_controle__(char, text[n+1])
                    force_continue = (controle == 14)
                else:
                    token = ''
                    controle = -1
            else: # se se nao é -1 
                yield(controle, token) # emitimos o token q temos 
                token = char
                controle = __get_controle__(char, text[n+1])
                force_continue = (controle == 14) # ja foi computado o próximo char, que é '*' e sem isso /*/ seria conciderado um comentário de bloco, para // não é problema pois o mesmo só para a busca, então não importa se paramos no 1º '/' ou no 2º
        
        # Percorre até o final do TMF
        elif (controle == 13): # token mal formado
            sep = __get_if_sep__(char, text[n+1], separadores = SEPARADORES, default_not_in = 13)
            if (sep[1] != 13): # se for um separador
                yield (controle, token)
                token = ''
            token += char
            controle = sep[1]

    # Gera o token com o estado atual quando termina o loop
    else: # else for, quando string acaba
        print(f' fim de string\t| Controle: {controle}\t|Token: {token}\t|Char Analizado: "{char if char else ""}"\t|erro_ponto: {erro_ponto}\t|force_continue: {force_continue}')
        for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
            yield token_gerado

# Gera o token correspondente para a lista de tokens
def __gera_token_saida__(controle, token, erro_ponto):
    if (controle in [3, 9]):
        yield (9, token)
    elif (controle in [2, 12]):
        yield (controle if token not in PRE else 1, token) # se o controle for 12 o token não vai ta em PRE, logo só lança 2 se o token for PRE
    elif (controle in [4, 11]):
        yield (controle if erro_ponto != False  else 11, token)
    elif (4 < controle < 9):
        yield (controle, token) # não verificamos, pois temos o que ele é, e nao existe próximo char
    elif (controle == 13):
        yield (controle, token)
    elif (controle == 14):
        raise comentario_bloco_excption(token)

def __get_if_sep__(char, next, separadores = SEPARADORES, default_not_in = 12):
    if (char + next in separadores):
        return (char + next, separadores.get(char + next, default_not_in)) # default nunca sera retornado pois o if garnate que ta no dicionario
    return (char, separadores.get(char, default_not_in))

# Identifica o estado de acordo com o caracter atual e próximo
def __get_controle__(char, next):
    if (char in ascii_letters):
        controle = 2
    elif (char in digits):
        controle = 4
    elif (char == '"'):
        controle = 3
    elif (char == '/' and next == '*'):
        controle = 14
    elif (char == '/' and next == '/'):
        controle == 15
    elif (search(r'\s', char)):
        controle = -1
    else:
        sep = __get_if_sep__(char, next, separadores = SEPARADORES, default_not_in = 13)
        controle = sep[1]
    return controle

if __name__ == '__main__':
    # s = '/*/'
    # s = '++'
    # s = '3&.+a 3&&&.'
    s = ''
    for a in get_tokens(s):
        print(a)