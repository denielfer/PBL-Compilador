
class erro_sintaico(Exception):
    pass

class file_end(Exception):
    pass

get_functions = {
    'const':[[{"key":'token',"value":'const','next':('const'   ,1)}],
             [{"key":'token',"value":'{'    ,'next':('const'   ,2)}],
             [{"key":'token',"value":'}'    ,'next':('variables',0)}]],
    'variables':[[{"key":'token',"value":'variables','next':('variables'   ,1)}],
                [{"key":'token',"value":'{'       ,'next':('variables'   ,2)}],
                [{"key":'token',"value":'}'       ,'next':('END','')}]],
}


def analize(get_token:iter):
    stack = [("const",0)]
    for token in get_token:
        print(f'token: {token}\t| stack:{stack}')
        stage,pos_stage = stack.pop(-1)
        flag = True # se tiver produção vazia continuamos a analize com o mesmo token
        while flag: # ta aqui pra suporta produção vazia
            flag = False
            if stage == 'END':
                raise erro_sintaico(f"Na linha {token['line']}, era esperado 'EOF' porém foi obtido {token['token']}")
            list_actions = get_functions[stage][pos_stage]
            esperado = []
            for action in list_actions: # para cada token na lista de tokens esperados
                print(f'Buscando:{action}',end='\t|')
                # print(token[action['key']],action["value"],token[action['key']] == action["value"])
                if token[action['key']] == action["value"]: # verifica se o token é o esperado
                    stack.append(action["next"])
                    print('True')
                    break
                elif action["value"] == "": # se for token vazio continuamos em busca pelo proximo elemento q vem
                    stage,pos_stage = action["value"]
                    flag = True
                else: # se nao é token esperado e o nao tem token vazio esperado adicionamos a lsita de esperados
                    esperado.append(action["value"])
                    print('False')
            else: # se nao acho ação para token é pq é token nao esperado
                raise erro_sintaico(f"Na linha {token['line']}, era esperado {esperado} porém foi obtido {token['token']}")
    else:
        print('acabou a lista de tokens logo erro')
        raise file_end('Lista de tokens acabou')