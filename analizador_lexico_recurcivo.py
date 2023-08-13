######################### TO DO ##########################
# fazer geração de tokens para itendificadores e palavras reservadas

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

# nao tem ponto pois este pode ser usado para gerar numero e pode dar problema ainda nao pensei em como seria entao ta fora ate o momento
# '/*' e '//' tem mesma ordem de prioridade assim escolhe-se quebra em '/*' e caso exista um '//' antes usa o raise Exception para cancelar o continuamento da função de analize para linha
prioridade = '/* // " ++ + -- -> - >= <= != == = ! && || * / < > [ ] { } ; ,'.split()

class comportamento:
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:object]):
        ...

def get_token(txt:str,chars_list: list[str],executions:dict[str:comportamento]):
    if chars_list == []:
        # print(f'Lista de caracteres a serem buscados acabou')
        return
    if txt.strip() == '':
        # print( f'string vazia para busca de {chars_list[0]}')
        return
    # print(f'A string \/{txt}\/ sera analizada para o token {chars_list[0]}',end=' | ')
    new_txt = txt.split(chars_list[0])
    # print('resultado: ',new_txt)#, f' para: {chars_list[0]}')
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
        for txt in txts:
            flag = False
            if '*/' in txt:
                for token in get_token(txt.split('*/',1)[1],chars_list[1:],executions):
                    yield token
                flag = True
        if flag is False:
            yield 10,None
        
class comentario_linha(comportamento):
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        raise comentario_linha_excption

class cadeia_de_caracter(comportamento):
    ########################## rever #################################################################
    def ação(txts:list[str],chars_list: list[str],executions:dict[str:comportamento]):
        if txts == []:
            return
        cadeia = ''
        flag = False
        for txt in txts:
            flag = False
            if '"' in txt:
                # NESTE NAO SE FAZ SPLIT E SIM PEGA DE UM ELEMENTO DO VETOR A OUTRA UMA VEZ QUE '"' ABRE E FECHA O ELEMENTO BUSCADO
                t = txt.split('"')
                cadeia += t[0]
                yield 3,cadeia + t[0]
                cadeia = ''
                for token in get_token(t[1:],chars_list[1:],executions):
                    yield token
                flag = True
            else:
                cadeia+=txt
        if flag is False:
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
    ',':operadores_delimitadores
}


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
    
    #teste para comentario de bloco
    #########TO DO #############################################################

    #teste para cadeia de caracteres
    s = '+/* // +-*/ -' # + , iguinora o que ta em comentario e termina com o - 
    for a in get_token(s,prioridade,comportamentos):
        print(a)