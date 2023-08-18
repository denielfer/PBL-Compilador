
#'1.' é erro,
from string import printable, ascii_letters, digits
from re import search,split,findall

tabela = {
        '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
        '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
        '!': 7, '&&': 7, '||': 7, 
        ';': 5, ',': 5, '.': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
    }

codigos = {
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

class comentario_linha_excption(Exception):
    pass

class comentario_bloco_excption(Exception):
    pass

# nao tem ponto pois este pode ser usado para gerar numero e pode dar problema ainda nao pensei em como seria entao ta fora ate o momento
# '/*' e '//' tem mesma ordem de prioridade assim escolhe-se quebra em '/*' e caso exista um '//' antes usa o raise Exception para cancelar o continuamento da função de analize para linha
prioridade = '++ + -- -> - >= <= != == = ! && || * / < > [ ] { } ( ) ; ,'.split()

def processar_string(txt:str, chars_list: list[str],rejex:bool = False):
    '''
        Esta função so existe pois 'numero.algo' se algo nao for um numero deve gerar erro, como isso impossibilita a geração
            do token que 'algo' seria temos primieramente identificamos este erro para depois seguir para os demais tokens 
            pois este tem maior prioridade uma vez q tem capacidade de interromper todos os outros tokens
    '''
    NMR = findall(i_pr_n.re_NMR,txt)
    txts = split(i_pr_n.re_NMR,txt)
    for token in processar_blocos(txts[0], chars_list = chars_list, rejex= False):
        yield token
    for n,txt in enumerate(txts[1:]):
        # print(NMR, n) 
        yield (11, NMR[n].strip())
        for token in processar_blocos(txt, chars_list = chars_list, rejex= False):
            yield token

def processar_blocos(txt:str, **kargs):
    '''
        Nesta função tratamos comentario de bloco, linha e cadeia de caracter, pois uma atrapalha 
            a outra dependendo da ordem de aparição
            
    '''
    cb = txt.find('/*')
    cl = txt.find('//')
    cc = txt.find('"')
    cb = cb if cb!=-1 else len(txt)+1
    cl = cl if cl!=-1 else len(txt)+1
    cc = cc if cc!=-1 else len(txt)+1
    # print(cb,cl,cc)
    while len(set([cb,cl,cc])) != 1: # se todos sao iguais entao nao achou, logo skipa o while
        if (cb < cl and cb < cc):
            txt = txt.split('/*',1)
            for token in get_token(txt[0], **kargs):
                yield token
            if '*/' in txt[1]:
                txt = txt[1].split('*/',1)[1]
            else:
                raise comentario_bloco_excption(txt[1])
        elif(cl < cb and cl < cc):
            txt = txt.split('//',1)
            for token in get_token(txt[0], **kargs):
                yield token
            raise comentario_linha_excption
        else: # se o primeiro nao foi os outros é comentario de bloco
            # print('--------')
            txt = txt.split('"',2) # tentamos quebra nos 2 '"'
            for token in get_token(txt[0], **kargs): # analizamos o token antes do 1 '"' e os emitimos
                yield token
            match len(txt):
                case 2: # se tiver 2 de tamanho o comentario nao ta fechado
                    yield 9,f'"{txt[1]}'
                    return
                case 3: # se tiver 3 de tamanho o comentario
                    for char in txt[1]:
                        if char not in printable: # se tiver caracter invalido emitimos o token de comentario mal formado
                            yield 9,f'"{txt[1]}"' 
                            break
                    else: # se chegou aqui nao tem caracter invalido entao emitimos o token de ok
                        yield  3,f'"{txt[1]}"'
                    txt = txt[2] # setamos o texto para proxima iteração do loop
        # variaveis pra procima iteração
        # print(txt)
        cb = txt.find('/*')
        cl = txt.find('//')
        cc = txt.find('"')
        cb = cb if cb!=-1 else len(txt)+1
        cl = cl if cl!=-1 else len(txt)+1
        cc = cc if cc!=-1 else len(txt)+1
        # print(cb,cl,cc)
    for token in get_token(txt, **kargs):
        yield token

def get_token(txt:str, chars_list: list[str],rejex:bool = False):
    if txt.strip() == '':
        # print( f'string vazia para busca de {chars_list[0]}')
        return
    if chars_list == []:
        # print(f'Lista de caracteres a serem buscados acabou')
        for token in i_pr_n.ação(txt, action = 1 if rejex else 0):
            yield token
        return
    txts = [txt]
    token_delimitadores = []
    for delimitador in chars_list:
        for n in range(len(txts))[::-1]:
            txt = txts.pop(n)
            new_txt = txt.split(delimitador)
            txts.insert(n, new_txt[-1])
            for txt in new_txt[-2::-1]:
                token_delimitadores.insert(n,delimitador)
                txts.insert(n, txt)
    for txt in txts:
        for token in i_pr_n.ação(txt, action = 1 if rejex else 0):
            yield token
        try:
            delimitador = token_delimitadores.pop(0)
            yield tabela[delimitador], delimitador
        except:
            pass

#Para variavel faz strip ( tira ' ' do inicio e fim, uma vez que no final temos um separador ), verifica se o primeiro char é digito ou letra, sendo letra segue pegando char ate o fim verificando se é valido ( letra + digito + '_') se nao for ver se é ' ' se for termina token se nao gera erro, se achar primeiro numero continua verificando numeros fim ou ' ' ou ponto, se ponto pega numero no proximo se nao gera erro, 
# para palavra reservada antes de emitir token de variavel ve se ta na lista de reservada
class i_pr_n(): # identificadores, palavras reservadas e numeros
    indent_char = ascii_letters + digits + '_'
    palavras_reservadas = ["variables", "const", "class", "methods","objects", 
                           "main", "return", "if", "else", "then", "for", "read", 
                           "print", "void", "int", "real", "boolean", "string", 
                           "true", "false"]
    def ação(txt:str, action:int = 0):
        txt = txt.strip()
        func = i_pr_n.__monta_token__ if action == 0 else i_pr_n.__monta_token_regex__
        while txt != '':
            # print(txt)
            tokens,txt = func(txt)
            for token in tokens:
                yield token
            txt = txt.strip()
                
    def __monta_token__(txt, n = 0):
        if txt == '':
            return [], ''
        tokens = []
        identificador = txt[n]
        if txt[n] in ascii_letters: # verifica indentificador ou palavra reservada
            erro = False
            for n,char in enumerate(txt[n+1:]):
                        if char in i_pr_n.indent_char:
                            identificador += char
                        elif char in ' .':
                            if erro:
                                tokens.append((12, identificador))
                            else:
                                if identificador in i_pr_n.palavras_reservadas:
                                    tokens.append((1, identificador))
                                else:
                                    tokens.append((2, identificador))
                            if char == '.':
                                tokens.append((5, char))
                            break
                        else:
                            erro = True
                            identificador += char
            else:
                if not erro:
                    if identificador in i_pr_n.palavras_reservadas:
                        tokens.append((1, identificador))
                    else:
                        tokens.append((2, identificador))
                else:
                    tokens.append((12, identificador))
        elif txt[n] in digits:# verifica numero
            erro = False
            last_dot = False
            digits_temp = digits + '.'
            for n, char in enumerate(txt[n+1:]):
                        if char in digits_temp:
                            last_dot = False
                            identificador += char
                        elif char in ' ':
                            if not erro and not last_dot:
                                tokens.append((4, identificador))
                            else:
                                tokens.append((11, identificador))
                            break
                        else:
                            erro = True
                            identificador += char
                        if char == '.':
                            last_dot = True
                            digits_temp = digits
            else:
                if not erro and not last_dot:
                    tokens.append((4, identificador))
                else:
                    tokens.append((11, identificador))
        else:#se nao é token mal formado
            # print(identificador,end ='->')
            if identificador != '.':
                for n, char in enumerate(txt[n+1:]):
                    # print(char,end ='->')
                    if char in ' .':
                        tokens.append((13, identificador))
                        if char == '.':
                            tokens.append((5, '.'))
                        # print()
                        break
                    else:
                        identificador += char
                else: # acabou a string com token mal formado gera o token
                    tokens.append((13, identificador))
            else:
                # print()
                n=n-1
                tokens.append((5, '.'))
        # print(txt,' -> ',txt[n+1:],tokens)
        return tokens, txt[n+2:]

    re_PRE = r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b'
    re_IDE = r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b'
    re_NRO = r'\b\d+(\.\d*)?\b'
    re_NMR = r'\b\d+\.[^\d|^\/*|^\/\/][\w\.]*'
    # re_NMR = r"\b\d+\.(?!\d*|\/\*|\/\/)([[\w\.]*)"
    
    def __monta_token_regex__(txt):
        if txt == '':
            return [], ''
        txt = txt.strip()
        tokens = []
        while txt != '':
            # print(txt)
        # for token in txt:
            result = search(i_pr_n.re_PRE, txt)
            if(result is None):
                result = search(i_pr_n.re_IDE, txt)
                if(result is None):
                    result = search(i_pr_n.re_NRO, txt)
                    if result is None:
                        result = search(r'\.', txt)
                        if result is None:
                            break
                        else:
                            #acho '.'
                            tokens.append((result, 5))
                            txt = txt[:result.start()] + txt[result.end():]
                    else:
                        #acho pre
                        tokens.append((result, 4))
                        txt = txt[:result.start()] + txt[result.end():]
                else:
                    #acho IND
                    tokens.append((result, 2))
                    txt = txt[:result.start()] + txt[result.end():]
            else:
                #acho pre
                tokens.append((result, 1))
                txt = txt[:result.start()] + txt[result.end():]
            txt = txt.strip()
        tokens.sort(key = lambda x: x[0].start(), reverse = False)
        retorno = []
        for token in tokens:
            # print(token[0].group())
            retorno.append((str(token[0].group()), token[1]))
        return retorno, ''

if __name__ == '__main__':
    # # Teste inicial para operadores e delimitadores
    # s='+-' 
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # # teste para varios delimitadores e operadores
    # s= '+-+-+-+-+-' 
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # # testando todos delimitadores e operadores
    # s = '+++---> - >=<=!====!&&||* /<>[]{};,' 
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # # teste para cometnario de linha
    # s = '+//as+as' # espera token + e erro 
    # print(s)
    # try:
    #     for a in processar_string(s,prioridade,):
    #         print(a)
    # except comentario_linha_excption:
    #     pass

    # # teste para cadeia de caracteres
    # s = '+/* // +-*/ -' # + , iguinora o que ta em comentario e termina com o - 
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # # teste identificador
    # s = 'a + = 1'
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)
    
    # # teste palavra reservada
    # s = 'for variables const+ class= 1 classconst'
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)
    
    # # teste erros erro identificador, erro numero e erro token
    # s = 'asd_12 asd.123 asds.. as@# 123 12.3 12..3 1.2.3 .3 1. @as %$#'
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # # teste erros erro identificador, erro numero e erro token
    # s = 'a "asdasdas'
    # print(s)
    # for a in processar_string(s,prioridade,):
    #     print(a)

    # #test rejex:
    # s = 'asd_12 asd.123 123 12.3 3.+ 2......... .2'
    # print(s)
    # for a in processar_string(s, prioridade, ):
    #     print(a)

    # #test rejex:
    # s = '3."asdasd 2.{asdasd 3.+123123+'
    # print(s)
    # for a in processar_string(s, prioridade, ):
    #     print(a)

    # # cadeia de caracter
    # s = '"asdasd// /*" "áa\zsdds/* //" "asdasd'
    # print(s)
    # for a in processar_string(s, prioridade):
    #     print(a)

    # cadeia de caracter
    s = '3./*ad*/ 3./*3*/3 &as&& &/**/& &as& "\n" "Ç" @.2 2@ 2.2@' 
    # 3. coment | 3. coment 3 | &as && | & & | &as& | "\n" | "Ç" | @ . 2
    print(s) # aparece 2 linhas porque o \n é usado como quebra de linha
    for a in processar_string(s, prioridade):
        print(a)
    