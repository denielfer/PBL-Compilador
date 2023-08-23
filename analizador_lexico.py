PRE =  ["variables", "const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for", "read", "print", "void", "int", "real","boolean", "string", "true", "false"]
from string import ascii_letters, digits, printable
from re import search
# printable= printable.replace('"','')
op_ar = ["+", "-", "*", '/', "++", "--"]
op_re = '!= == < <= > >= ='.split()
op_log = '! && ||'.split()
coment_cadeia = '"'
coment_block = ['/*']
coment_linha = ['//']
# SEPARADORES = op_ar+op_re+op_log+coment_cadeia+coment_block+coment_linha
IDE_CHAR = ascii_letters + '_' + digits 
digits_p = digits + '.'

SEPARADORES = { # separadores e seu codigo
        '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
        '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
        '!': 7, '&&': 7, '||': 7, 
        ';': 5, ',': 5, '.': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
        '"': 3,
    }

SEPARADORES_NUMERO = { # separadores e seu codigo
        '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
        '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
        '!': 7, '&&': 7, '||': 7, 
        ';': 5, ',': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
        '"': 3,
    }

# separadores = op_ar+op_re+op_log+coment_block+coment_linha

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

class comentario_bloco_excption(Exception):
    pass

def get_tokens(text):
    # print(text, len(text))
    text += '\n'
    token = ''
    controle = -1
    erro_ponto = None
    force_continue = False
    for n, char in enumerate(text[:-1]):
        print(f' {n}\t| Controle: {controle}\t|Token: {token}\t|Char Analizado: "{char}"\t|erro_ponto: {erro_ponto}\t|force_continue: {force_continue}')
        if force_continue:
            force_continue = False
            continue
        elif controle in [3, 9]:
            if char == '"':
                yield (controle, token + '"')
                token = ''
                controle = -1
                continue
            elif char not in printable:
                controle = 9
            token += char
        elif controle == 14: # comentario bloco
            if token[-1] + char == '*/':
                token = ''
                controle = -1
            else:
                token += char
        elif controle == 15: #comentario linha
            return
        elif char + text[n+1] == '//':
            return
        elif char + text[n+1] == '/*':
            for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
                yield token_gerado
            erro_ponto = None
            controle = 14
            force_continue = True
            token = '/*'
        elif(search(r'\s', char)):
            for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
                yield token_gerado
            erro_ponto = None # reseta erro de ponto de numero, pois caso seja teria valor
            token = ''
            controle = -1
        elif controle == -1:
            controle = __get_controle__(char, text[n+1]) # nao precisa do force continue para 14, pois esse acabou de ser verificado encima
            if controle != -1:
                token += char
        elif controle in [2, 12]:
            if char in IDE_CHAR: # se ainda é char valido em indentificador
                token += char
                continue
            sep = __get_if_sep__(char, text[n+1], default_not_in = 12)
            if sep[1] != 12: # se nao for char invalido, é separador 
                yield (1 if token in PRE else controle, token)  # geramos IDE ou PRE
                token = '' # limpamos o token q esta sendo gerado
            token += char
            controle = sep[1]
        elif controle in [4, 11]:
            if char in digits_p:
                if erro_ponto == False:
                    erro_ponto = True
                token += char
                if char == '.':
                    if erro_ponto is None:
                        erro_ponto = False
                    else:
                        controle = 11
                continue
            elif erro_ponto == False: # precisa especificar se é false pois (not erro_ponto) triga no None
                #consome o token logo apos o '.' se nao estiver em digits
                token += char
                erro_ponto = True
                controle = 11
                continue
            sep = __get_if_sep__(char, text[n+1], separadores = SEPARADORES_NUMERO, default_not_in = 11)
            if sep[1] != 11: # 11 seria nao achar separador, entao entra no if se achar separador
                yield (controle, token)
                token = ''
                erro_ponto = None
            token += char
            controle = sep[1]
        elif 4 < controle < 9: # separadores e delimitadores#####################################################################################
            sep = __get_if_sep__(token, char, separadores = SEPARADORES, default_not_in = -1)
            if sep[1] != -1:
                yield (sep[1], sep[0])
                if len(sep[0]) == 1: # se achou separador de 2 char entao ja emitiu para esse char, se nao precisamos descobri o que ele é
                    token = char
                    controle = __get_controle__(char, text[n+1])
                    force_continue = controle == 14
                else:
                    token = ''
                    controle = -1
            else: # se se nao é -1 
                yield(controle, token)# emitimos otoken q temos 
                token = char
                controle = __get_controle__(char, text[n+1])
                force_continue = controle == 14 # ja foi computado o proximo char, que é '*' e sem isso /*/ seria conciderado um comentario de bloco, para // nao é problema pois o mesmo so para a busca, entao nao importa se paramos no 1º '/' ou no 2º
        elif controle == 13: # token mal formado
            sep = __get_if_sep__(char, text[n+1], separadores = SEPARADORES, default_not_in = 13)
            if sep[1] != 13: # se for um separador
                yield (controle, token)
                token = ''
            token += char
            controle = sep[1]
    else: # else for, quando string acaba
        for token_gerado in __gera_token_saida__(controle, token, erro_ponto):
            yield token_gerado

def __gera_token_saida__(controle, token, erro_ponto):
    if controle in [3, 9]:
        yield (9, token)
    elif controle in [2, 12]:
        yield (controle if token not in PRE else 1, token) # se 12 o token nao vai ta em PRE, logo so solta 2 se token for PRE
    elif controle in [4, 11]:
        yield (controle if erro_ponto != False  else 11, token)
    elif 4 < controle < 9:
        yield (controle, token) # nao verificamos pois temos o que ele é, e nao existe proximo char
    elif controle == 13:
        yield (controle, token)
    elif controle == 14:
        raise comentario_bloco_excption(token)


def __get_if_sep__(char, next, separadores = SEPARADORES, default_not_in = 12):
    if char + next in separadores:
        return (char + next, separadores.get(char + next, default_not_in)) # default nunca sera retornado pois o if garnate que ta no dicionario
    return (char, separadores.get(char, default_not_in))

def __get_controle__(char,next):
    if char in ascii_letters:
        controle = 2
    elif char in digits:
        controle = 4
    elif char == '"':
        controle = 3
    elif char == '/' and next == '*':
        controle = 14
    elif char == '/' and next == '/':
        controle == 15
    elif search(r'\s', char):
        controle = -1
    else:
        sep = __get_if_sep__(char, next, separadores = SEPARADORES, default_not_in = 13)
        controle = sep[1]
    return controle

if __name__ == '__main__':
    s = '1++'
    for a in get_tokens(s):
        print(a)