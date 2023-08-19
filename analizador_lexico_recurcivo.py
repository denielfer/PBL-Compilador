from string import printable, ascii_letters, digits
from re import search, split, findall,escape

# Separadores: elementos usados para indicar o fim de um token e inicio de outro, sendo eles: operadores, delimitadores, ' ', '/*','"' e '//'
#   Excessoes: 'numero.algo', '.' para numero, Cadeia de Caracter so tem '"' de separador
tabela = { # separadores e seu codigo
        '+': 8, '-': 8, '*': 8, '/': 8, '++': 8, '--': 8, 
        '!=': 6, '==': 6, '<': 6, '<=': 6, '>': 6, '>=': 6, '=': 6,
        '!': 7, '&&': 7, '||': 7, 
        ';': 5, ',': 5, '.': 5, '(': 5, ')': 5, '[': 5, ']': 5, '{': 5, '}': 5, '->': 5,
    }

codigos = { # tabela de codigos gerados para tokens
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

def processar_string(txt:str, chars_list:list[str], rejex:bool = False):
    '''
        Esta função so existe pois 'numero.algo' se algo nao for um numero deve gerar erro, como isso impossibilita a geração
            do token que 'algo' seria temos primieramente identificamos este erro para depois seguir para os demais tokens 
            pois este tem maior prioridade uma vez q tem capacidade de interromper todos os outros tokens

        Pelo regex so é aceito depois de 'numero.' outro numero, '/*' e '//', ser aceito significa nao ser processado nessa função
    '''
    NMR = findall(i_pr_n.re_NMR, txt)
    txts = split(i_pr_n.re_NMR, txt)
    for token in processar_blocos(txts[0], chars_list = chars_list, rejex = False):
        yield token
    for n,txt in enumerate(txts[1:]):
        # print(NMR, n) 
        yield (11, NMR[n].strip())
        for token in processar_blocos(txt, chars_list = chars_list, rejex = False):
            yield token

def processar_blocos(txt:str, **kargs):
    '''
        Nesta função tratamos comentario de bloco, linha e cadeia de caracter, pois uma atrapalha 
            a outra dependendo da ordem de aparição
            
    '''
    cb = txt.find('/*')
    cl = txt.find('//')
    cc = txt.find('"')
    cb = cb if cb != -1 else len(txt) + 1
    cl = cl if cl != -1 else len(txt) + 1
    cc = cc if cc != -1 else len(txt) + 1
    # print(cb,cl,cc)
    while len(set([cb, cl, cc])) != 1: # se todos sao iguais entao nao achou, logo skipa o while
        if (cb < cl and cb < cc):
            txt = txt.split('/*', 1)
            for token in get_token(txt[0], **kargs):
                yield token
            if '*/' in txt[1]:
                txt = txt[1].split('*/', 1)[1]
            else:
                raise comentario_bloco_excption(txt[1])
        elif(cl < cb and cl < cc):
            txt = txt.split('//', 1)
            for token in get_token(txt[0], **kargs):
                yield token
            raise comentario_linha_excption
        else: # se o primeiro nao foi os outros é comentario de bloco
            # print('--------')
            txt = txt.split('"', 2) # tentamos quebra nos 2 '"'
            for token in get_token(txt[0], **kargs): # analizamos o token antes do 1 '"' e os emitimos
                yield token
            match len(txt):
                case 2: # se tiver 2 de tamanho o comentario nao ta fechado
                    yield 9, f'"{txt[1]}'
                    return
                case 3: # se tiver 3 de tamanho o comentario
                    for char in txt[1]:
                        if char not in printable: # se tiver caracter invalido emitimos o token de comentario mal formado
                            yield 9, f'"{txt[1]}"' 
                            break
                    else: # se chegou aqui nao tem caracter invalido entao emitimos o token de ok
                        yield 3, f'"{txt[1]}"'
                    txt = txt[2] # setamos o texto para proxima iteração do loop
        # variaveis pra procima iteração
        # print(txt)
        cb = txt.find('/*')
        cl = txt.find('//')
        cc = txt.find('"')
        cb = cb if cb != -1 else len(txt) + 1
        cl = cl if cl != -1 else len(txt) + 1
        cc = cc if cc != -1 else len(txt) + 1
        # print(cb,cl,cc)
    for token in get_token(txt, **kargs):
        yield token

def get_token(txt:str, chars_list:list[str], rejex:bool = False):
    '''
        Aqui lidamos com os separadores, quebrando a string em partes menores e lidando com essas partes
    '''
    if txt.strip() == '': # se ta vazia retorna
        # print( f'string vazia para busca de {chars_list[0]}')
        return
    if chars_list == []: # se a lista de separadores ta vazia fazemos analize de IDE PRE NRO E TMF
        # print(f'Lista de caracteres a serem buscados acabou')
        for token in i_pr_n.ação(txt, action = 1 if rejex else 0):
            yield token
        return
    txts = [txt]
    token_delimitadores = []
    for delimitador in chars_list: # para cada delimitador
        for n in range(len(txts))[::-1]: 
            '''
                temos um vetor x/ x é composto de n-strings assim percoremos ele de tras pra frente para processar 
                    cada string e colocar o resultado inplace. Assim nao precisamos ficar mudando o vetor no codigo
                    e como estamos na ordem invertida nao pre cisa de matemagia para ajusta indicec dos nao processados
            '''
            txt = txts.pop(n) 
            new_txt = txt.split(delimitador)
            txts.insert(n, new_txt[-1]) # split nescessariamente tem elemento 0, assim pelo menos 1 elemento existe
            '''
                mesma logica do loop de cima, começa em -2 pq ja processamos o -1 encima, assim podemos no mesmo loop adicionar 
                    o delimitador que gerou essa divisao na string no seu vetor e a sub-string. assim lidamos com o fato de 
                    que esse delimitador fica sempre entre 2 substrings geradas pelo split. 
            '''
            for txt in new_txt[-2::-1]:
                token_delimitadores.insert(n, delimitador)
                txts.insert(n, txt)
    for txt in txts: # depois de lidarmos com todos os delimitadores precisamos processar cada string 
        for token in i_pr_n.ação(txt, action = 1 if rejex else 0):
            yield token
        try: # apos gerarmos os tokens para a substring liberamos o delimitador que foi responsavel pela sub-divisão
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
        txt = txt.strip()  # remove ' ' do inicio e fim
        func = i_pr_n.__monta_token__ if action == 0 else i_pr_n.__monta_token_regex__
        while txt != '': # enquanto tiver coisas na string
            # print(txt)
            tokens, txt = func(txt) # pegamos a primeira lista de token da string, pois existem casos onde mais de 1 sao geradas. ex:'@.'
            for token in tokens:
                yield token
            txt = txt.strip() # limpamos inicio e fim dos ' ' para continuar analize
                
    def __monta_token__(txt, n = 0):
        '''
            Esta função avalia uma string se tem IDE, PRE, NRO, NMF, TMF e emite delimitador '.'
        '''
        if txt == '':
            return [], ''
        tokens = []
        identificador = txt[n] # sempre so pega tokens apartir do 1 char, e so olha ate o final deste token, gerando possivel token ligado. ex:'@.'
        if txt[n] in ascii_letters: # verifica indentificador ou palavra reservada
            erro = False
            for n, char in enumerate(txt[n+1:]):
                        if char in i_pr_n.indent_char:
                            identificador += char
                        elif char in ' .': # se acho um dos separadores que sobrou
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
                        else: # se nao é char valido pra identificador ou um dos separadores q sobrou é char q gera erro no identificador
                            erro = True
                            identificador += char
            else: # se olhou a string inteira e nao acabou o token de identificador
                if not erro:
                    if identificador in i_pr_n.palavras_reservadas:
                        tokens.append((1, identificador))
                    else:
                        tokens.append((2, identificador))
                else:
                    tokens.append((12, identificador))
        elif txt[n] in digits:# verifica numero
            '''
                Aqui nao analiza so analiza erro de numero ter mais de 1 '.' pois os demias de '.' sao pegos em processar_string()
            '''
            erro = False
            digits_temp = digits + '.'
            for n, char in enumerate(txt[n+1:]):
                if char in digits_temp:
                    identificador += char
                elif char == ' ': # neste caso so sobra o separador ' '
                    if not erro:
                        tokens.append((4, identificador))
                    else:
                        tokens.append((11, identificador))
                    break
                else: # pegou algum char q nao é separador ou numero da erro
                    erro = True
                    identificador += char
                if char == '.': # se acho um ponto, qualquer ponto que vinher vai gerar erro, pois ele é removido da lista de aceitos
                    digits_temp = digits
            else:# se acabou a string e nao gerou token do numero
                if not erro:
                    tokens.append((4, identificador))
                else:
                    tokens.append((11, identificador))
        else:#se nao, so sobra token mal formado ou '.' de delimitador
            # print(identificador,end ='->')
            if identificador != '.': # se pegou '.' é delimitador entao so buscamos mais caractesres se nao for '.'
                for n, char in enumerate(txt[n+1:]):
                    # print(char,end ='->')
                    if char in ' .': # separadores restantes para estes casos
                        # se o separador é '.' geramos o token mal formado e o token do '.'
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
                #se o 1 elemento do vetor é '.', geramos o token e passamos para a proxima busca começar no elemento seguinte
                # print()
                n = n - 1 # -1 póis no retorno a sub-string para proxima busca assume que pegou o proximo elemento ja
                tokens.append((5, '.'))
        # print(txt,' -> ',txt[n+1:],tokens)
        return tokens, txt[n+2:]

    re_PRE = r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b'
    re_IDE = r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b'
    re_NRO = r'\b\d+(\.\d*)?\b'
    string = '++ + -- -> - >= <= != == = ! && || * / < > [ ] { } ( ) ; ,'
    re_NMR = r'\b\d+\.[^\d|^\/*|^\/\/]'
    re_NMR = f"{re_NMR}([{escape(string)}])"

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
    # s = '3./*ad*/ 3./*3*/3 &as&& &/**/& &as& "\n" "Ç" @.2 2@ 2.2@' 
    # s = ' 3.3.3 6.a35#.99; 2.2. 1.1.1.! 9.0.0 10'
    s = '6.a35#.99;'
    # 3. coment | 3. coment 3 | &as && | & & | &as& | "\n" | "Ç" | @ . 2
    print(s) # aparece 2 linhas porque o \n é usado como quebra de linha
    for a in processar_string(s, prioridade):
        print(a)
    