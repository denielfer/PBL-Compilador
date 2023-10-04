
class erro_sintaico(Exception):
    pass

class file_end(Exception):
    pass

TYPE = ['int', 'real', 'boolean', 'string']
TYPES = TYPE +['void'] # menos IDE

get_functions = {
    'const':[{"test":[{"key":'token',"value":['const'],'next':[('const',1)]}],'erro':{'tipo_recuperação':'next'}},
             {"test":[{"key":'token',"value":['{'],'next':[('end_block',0)]}],'erro':{'tipo_recuperação':'next'}},
            ],
    'variables':[
                {"test":[{"key":'token',"value":['variables'],'next':[('variables',1)]}],'erro':{'tipo_recuperação':'next'}},
                {"test":[{"key":'token',"value":['{'],'next':[('end_block',0)]}],'erro':{'tipo_recuperação':'next'}},
                ],
    'class': [
              {"test":[{'key':'token',"value":['class'],'next':[('class',1)]}],'erro':{'tipo_recuperação':'next'}},
              {"test":[
                {'key':'token',"value":['main'],'next':[('end_block',0),('class',4)]},
                {'key':'type',"value":['IDE'],'next':[('end_block',0),('constructor',0),('class',2)]}
                ],'erro':{'tipo_recuperação':'next'}},
              {"test":[{'key':'token',"value":['extends'],'next':[("class",3)]},
                       {'key':'token',"value":[''],'next':[("class",4)]},
                       ],'erro':{'tipo_recuperação':'next'}},
              {"test":[{'key':'type',"value":['IDE'],'next':[("class",4)]}],'erro':{'tipo_recuperação':'next'}},
              {"test":[{'key':'token',"value":['{'],'next':[('methods',0),('object',0),("variables",0)]}],'erro':{'tipo_recuperação':'next'}}
              ],
    'object':[
                {"test":[{"key":'token',"value":['objects'],'next':[('object',1)]}],'erro':{'tipo_recuperação':'next'}},
                {"test":[{"key":'token',"value":['{'],'next':[('end_block',0)]}],'erro':{'tipo_recuperação':'next'}},
                ],
    'methods' :[ 
                {"test":[
                   {'key':'token',"value":['methods'],'next':[('methods',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'key':'token',"value":['{'],'next':[('end_block',0),('func_dec',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
               ],
    'func_dec':[
                {'test':[
                        {'key':'token',"value":TYPES,'next':[('func_dec',1)]},
                        {'key':'type',"value":['IDE'],'next':[('func_dec',1)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'key':'type',"value":['IDE'],'next':[('func_dec',0),('func_dec',2)]},
                        {'key':'token',"value":['main'],'next':[('func_dec',2)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'key':'token',"value":['('],'next':[('func_dec',3)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'key':'token',"value":[')'],'next':[('func_dec',4)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'key':'token',"value":['{'],'next':[('end_block',0),('return',0),('object',0),('variables',0)]},
                    ],'erro':{'tipo_recuperação':'next'}},
    ],
    'return':[
                {"test":[
                    {"key":'token',"value":['return'],'next':[('return',1)]}],'erro':{'tipo_recuperação':'next'}
                },
                {"test":[
                        {"key":'token',"value":[''],'next':[('return',2)]},
                    ],'erro':{'tipo_recuperação':'next'}
                },
                {"test":[
                    {"key":'token',"value":[';'],'next':[]}],'erro':{'tipo_recuperação':'next'}
                },
            ],
    'end_block':[
                {"test":[{"key":'token',"value":['}'],'next':[]}],'erro':{'tipo_recuperação':'next'}}
                ],
    'tipos_basicos':[
                {
                    'test':[
                            {'key':'token',"value":['int'],'next':[]},
                            {'key':'token',"value":['boolean'],'next':[]},
                            {'key':'token',"value":['real'],'next':[]},
                            {'key':'token',"value":['string'],'next':[]},
                        ],'erro':{'tipo_recuperação':'next'}
                    },
                ],
    "modelo" : [ 
                {"test":[
                ],'erro':{'tipo_recuperação':'next'}}
               ],
}


def analize(get_token:list):
    stack = [('END',0),('class',0),('variables',0),("const",0)]
    for token in get_token:
        print(f'token: {token}\t| stack:{stack}')
        stage,pos_stage = stack.pop(-1)
        flag = True # se tiver produção vazia continuamos a analize com o mesmo token
        while flag: # ta aqui pra suporta produção vazia
            flag = False
            if stage == 'END':
                yield f"Na linha {token['line']}, era esperado 'EOF' porém foi obtido {token['token']}"
                continue
            list_actions = get_functions[stage][pos_stage]['test']
            esperado = []
            for action in list_actions: # para cada token na lista de tokens esperados
                print(f'Buscando:{action}',end='\t|')
                # print(token[action['key']],action["value"],token[action['key']] == action["value"])
                if token[action['key']] in action["value"]: # verifica se o token é o esperado
                    for item in action["next"]:
                        stack.append(item)
                    print('True')
                    break
                # pode dar merda se vazil nao for o primeiro token
                elif "" in action["value"]: # se for token vazio continuamos em busca pelo proximo elemento q vem
                    print('True')
                    stage,pos_stage = action["next"][-1]
                    flag = True
                    break
                else: # se nao é token esperado e o nao tem token vazio esperado adicionamos a lsita de esperados
                    esperado += action["value"] 
                    print('False')
            else: # se nao acho ação para token é pq é token nao esperado
                if get_functions[stage][pos_stage]['erro']['tipo_recuperação'] == 'next':
                    print(f'modo thiago segue pra frente -> Na linha {token["line"]}, era esperado {esperado} porém foi obtido {token["token"]}')
                    for item in list_actions[-1]["next"]: # adiciona a pilha a ultima possibilidade do token
                        stack.append(item)
                yield f"Na linha {token['line']}, era esperado {esperado} porém foi obtido {token['token']}"
    else:
        stage,pos_stage = stack.pop(-1)
        if stage != 'END':
            list_actions = get_functions[stage][pos_stage]['test']
            esperado = []
            for action in list_actions:
                esperado += action["value"] 
            # print (f"Na linha {token['line']+1}, era esperado {esperado} porém foi obtido 'EOF'")
            yield f"Na linha {token['line']+1}, era esperado {esperado} porém foi obtido 'EOF'"
            print(f'acabou a lista de tokens e stack é {stage} logo erros de esperado mas erro de fim de arquivo')
        