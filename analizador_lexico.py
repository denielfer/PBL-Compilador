palavras_reservadas=  ["variables", "const", "class", "methods", "objects", "main", "return", "if", "else", "then", "for", "read", "print", "void", "int", "real","boolean", "string", "true", "false"]
from string import ascii_letters, digits, printable
# printable= printable.replace('"','')
op_ar = ["+", "-", "*", '/', "++","--"]
op_re = '!= == < <= > >= ='.split()
op_log = '! && ||'.split()
coment_cadeia = '"'
coment_block = ['/*','*/']
coment_linha = '//'
 

separadores = op_ar+op_re+op_log+coment_block+coment_linha

codigos = {
    1:'PRE',
    2:'IDE',
    3:'CAC',
    4:'NRO',
    5:'DEL',
    6:'REL',
    7:'LOG',
    8:'ART',
    9:'CMF',
    10:'CoMF',
    11:'NMF',
    12:'IMF',
    13:'TMF'
}

def analizar(text):
    txt = ''
    last = None
    controle = -1
    for char in text:
        if char in printable:
            if char == '"':
                if controle == 9:
                    yield txt,controle
                else:
                    yield txt,controle
                    controle = 9
                    txt = char
            if char in separadores:
                if controle <3:
                    yield txt,controle
                controle=4
                if last+char in separadores:
                    pass

