
from string import printable, ascii_letters, digits
from re import search,match

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

class comentario_linha_excption(Exception):
    pass

class comentario_bloco_excption(Exception):
    pass

# nao tem ponto pois este pode ser usado para gerar numero e pode dar problema ainda nao pensei em como seria entao ta fora ate o momento
# '/*' e '//' tem mesma ordem de prioridade assim escolhe-se quebra em '/*' e caso exista um '//' antes usa o raise Exception para cancelar o continuamento da função de analize para linha
prioridade = '/* // " ++ + -- -> - >= <= != == = ! && || * / < > [ ] { } ( ) ; ,'.split()

class comportamento:
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:object]):
        ...

def get_token(txt:str,chars_list: list[str],executions:dict[str:comportamento]):
    if txt.strip() == '':
        # print( f'string vazia para busca de {chars_list[0]}')
        return
    if chars_list == []:
        # print(f'Lista de caracteres a serem buscados acabou')
        for token in i_pr_n.ação(txt,chars_list,executions):
            yield token
        return
    # print(f'A string \/{txt}\/ sera analizada para o token {chars_list[0]}',end=' | ')
    new_txt = txt.split(chars_list[0])
    # print('resultado: ',new_txt, f' para: {chars_list[0]}')
    for token in get_token(new_txt[0],chars_list[1:],executions):
        yield token
    if new_txt[1:] != []:
        for token in executions[chars_list[0]].ação(new_txt[1:],chars_list,executions):
            yield token

class comentario_bloco(comportamento): 
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        flag = False
        t = ''
        for txt in txts:
            flag = False
            if '*/' in txt:
                for token in get_token(txt.split('*/',1)[1],chars_list[1:],executions):
                    yield token
                flag = True
                t=''
            else:
                t+=txt
        if flag is False:
            raise comentario_bloco_excption(t)
        
class comentario_linha(comportamento):
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        raise comentario_linha_excption

class cadeia_de_caracter(comportamento):
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        cadeia = '"'
        flag = True # true = precisa acha cadeia # indica se o pedaço do vetor vem de abertura de '"' ou da de fechamento
        quebrado = False
        for txt in txts:
            if flag:
                flag = False  # cadeia achada
                for char in txt:
                    if char not in printable:
                        quebrado = True
                    cadeia += char 
            else:
                flag = True # precisa acha cadia na proxima iteração
                if quebrado: # se a cadeia foi fechada e existe erro dentre os caracteres dela, geramos token de erro
                    yield 9,cadeia+'"'
                    quebrado = False
                else:# se a cadeia passada fecho e nao tem erro emitimos o token
                    yield 3,cadeia+'"'
                cadeia = '"'
                if txt == '':
                    continue
                for token in get_token(txt,chars_list[1:],executions):
                    yield token
        if not flag: # se terminou sem precisar acha cadeia de caracter quer dizer q nao foi fechado
            yield 9,cadeia

class operadores_delimitadores(comportamento):
    tabela = {
        '+':8, '-':8, '*':8, '/':8, '++':8, '--':8, 
        '!=':6, '==':6, '<':6, '<=':6, '>':6, '>=':6, '=':6,
        '!':7, '&&':7, '||':7, 
        ';':5, ',':5, '.':5, '(':5, ')':5, '[':5, ']':5, '{':5, '}':5, '->':5,
    }
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        # retorna o tokem pois é o elemento do meio do vetor da analize acima
        # ex: string: '+-+', buscando '-' no get token gera ['+','+'], ja se rodou o get_token para o index 0, entao emitimos o token encontrado que fica entre o index 0 e 1
        # o mesmo acontece para string: '-', buscando '-', gera ['',''], faz busca dos proximos em index 0, emite o token do -, faz a busca dso tokens para index 1
        # de forma similar para quando temos vetores maiores, a emição do token que fez o split acontece entre as analizes das strigns splitadas
        # como temos que gerar este token sempre entre os elementos do vetor, e o 1 elemtno do vetor é analizado na função que chama essa, basta iterarmos pelas posições restantes do vetor e emitir um token antes da analize daquela posição caso ela exista, caso nao exista o loop nao sera executado
        for txt in txts:
            yield operadores_delimitadores.tabela[chars_list[0]],chars_list[0]
            for token in get_token(txt,chars_list[1:],executions):
                yield token
        # print(f'Fim da emição de tokens para {chars_list[0]}')

comportamentos = {
    '/*':comentario_bloco,
    '//':comentario_linha,
    '"':cadeia_de_caracter,
    '++':operadores_delimitadores,
    '+':operadores_delimitadores,
    '--':operadores_delimitadores,
    '->':operadores_delimitadores,
    '-':operadores_delimitadores,
    '>=':operadores_delimitadores,
    '<=':operadores_delimitadores,
    '!=':operadores_delimitadores,
    '==':operadores_delimitadores,
    '=':operadores_delimitadores,
    '!':operadores_delimitadores,
    '&&':operadores_delimitadores,
    '||':operadores_delimitadores,
    '*':operadores_delimitadores,
    '/':operadores_delimitadores,
    '<':operadores_delimitadores,
    '>':operadores_delimitadores,
    '[':operadores_delimitadores,
    ']':operadores_delimitadores,
    '{':operadores_delimitadores,
    '}':operadores_delimitadores,
    ';':operadores_delimitadores,
    ',':operadores_delimitadores,
    '(':operadores_delimitadores,
    ')':operadores_delimitadores,
}
#Para variavel faz strip ( tira ' ' do inicio e fim, uma vez que no final temos um separador ), verifica se o primeiro char é digito ou letra, sendo letra segue pegando char ate o fim verificando se é valido ( letra + digito + '_') se nao for ver se é ' ' se for termina token se nao gera erro, se achar primeiro numero continua verificando numeros fim ou ' ' ou ponto, se ponto pega numero no proximo se nao gera erro, 
# para palavra reservada antes de emitir token de variavel ve se ta na lista de reservada
class i_pr_n(comportamento): # identificadores, palavras reservadas e numeros
    indent_char = ascii_letters + digits + '_'
    palavras_reservadas = ["variables", "const", "class", "methods","objects", 
                           "main", "return", "if", "else", "then", "for", "read", 
                           "print", "void", "int", "real", "boolean", "string", 
                           "true", "false"]
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        txt = txts.strip()
        while txt != '':
            # print(txt)
            tokens,txt = i_pr_n.__monta_token_regex__(txt)
            for token in tokens:
                yield token
            txt = txt.strip()

                
    def __monta_token__(txt, n = 0):
        if txt == '':
            return [],''
        tokens = []
        identificador = txt[n]
        if txt[n] in ascii_letters: # verifica indentificador ou palavra reservada
            erro = False
            for n,char in enumerate(txt[n+1:]):
                        if char in i_pr_n.indent_char:
                            identificador += char
                        elif char in ' .':
                            if not erro:
                                if identificador in i_pr_n.palavras_reservadas:
                                    tokens.append((1, identificador))
                                else:
                                    tokens.append((2, identificador))
                            else:
                                tokens.append((12,identificador))
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
                    tokens.append((12,identificador))
        elif txt[n] in digits:# verifica numero
            erro = False
            digits_temp = digits+'.'
            for n,char in enumerate(txt[n+1:]):
                        if char in digits_temp:
                            identificador += char
                        elif char in ' ':
                            if not erro:
                                tokens.append((4, identificador))
                            else:
                                tokens.append((11,identificador))
                            break
                        else:
                            erro = True
                            identificador += char
                        if char == '.':
                            digits_temp = digits
            else:
                if not erro:
                    tokens.append((4, identificador))
                else:
                    tokens.append((11,identificador))
        else:#se nao é token mal formado
            for n,char in enumerate(txt[n+1:]):
                if char == ' ':
                    tokens.append((13,identificador))
                    break
                else:
                    identificador += char
            else:
                if identificador == '.':
                    tokens.append((5,'.'))
                else:
                    tokens.append((13,identificador))

        # print(txt,' -> ',txt[n+1:],tokens)
        return tokens, txt[n+2:]

    re_PRE = r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b'
    re_IDE = r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b'
    re_NRO = r'\b\d+\.?\d*\b'
    
    def __monta_token_regex__(txt):
        if txt == '':
            return [],''
        txt = txt.strip()
        tokens = []
        while txt != '':
        # for token in txt:
            result = search(i_pr_n.re_PRE, txt)
            if( result is None ):
                result = search(i_pr_n.re_IDE, txt)
                if( result is None ):
                    result = search(i_pr_n.re_NRO, txt)
                    if result is None:
                        result = search(r'\.', txt)
                        if result is None:
                            break
                        else:
                            #acho '.'
                            tokens.append((result,5))
                            txt = txt[:result.start()] + txt[result.end():]
                    else:
                        #acho pre
                        tokens.append((result,4))
                        txt = txt[:result.start()] + txt[result.end():]
                else:
                    #acho IND
                    tokens.append((result,2))
                    txt = txt[:result.start()] + txt[result.end():]
            else:
                #acho pre
                tokens.append((result,1))
                txt = txt[:result.start()] + txt[result.end():]
            txt = txt.strip()
        tokens.sort(key=lambda x: x[0].start(), reverse=True)
        retorno = []
        for token in tokens:
            print(token[0].group())
            retorno.append((str(token[0].group()),token[1]))
        return retorno, ''


                                                


if __name__ == '__main__':
    # Teste inicial para operadores e delimitadores
    # s='+-' 
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    # teste para varios delimitadores e operadores
    # s= '+-+-+-+-+-' 
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    # testando todos delimitadores e operadores
    # s = '+++---> - >=<=!====!&&||* /<>[]{};,' 
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    # teste para cometnario de linha
    # s = '+//as+as' # espera token + e erro 
    # print('analizando: ', s)
    # try:
    #     for a in get_token(s,prioridade,comportamentos):
    #         print(a)
    # except comentario_linha_excption:
    #     pass

    #teste para cadeia de caracteres
    # s = '+/* // +-*/ -' # + , iguinora o que ta em comentario e termina com o - 
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    #teste identificador
    # s = 'a + = 1'
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)
    
    #teste palavra reservada
    # s = 'for variables const+ class= 1 classconst'
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)
    
    #teste erros erro identificador, erro numero e erro token
    # s = 'asd_12 asd.123 asds.. as@# 123 12.3 12..3 1.2.3 .3 1. @as %$#'
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    #teste erros erro identificador, erro numero e erro token
    # s = 'a "asdasdas'
    # for a in get_token(s,prioridade,comportamentos):
    #     print(a)

    #test rejex:
    s = 'asd_12 asd.123 123 12.3'
    for a in get_token(s,prioridade,comportamentos):
        print(a)
