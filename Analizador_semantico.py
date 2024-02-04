import copy

def init():
    global tabela,scopo, erro_sem, erros_semantico
    tabela = {'global':{},'stack':[]}
    scopo = ["global"]
    erro_sem = None
    erros_semantico = []

from analizador_sintatico import TYPE,TYPES,ART,ART_DOUBLE,REL, LOG, BOOL

def analize(stage,pos_stage,action,token,log_sem= None):
    if not log_sem:
        from sys import stdout
        log_sem = stdout
    global erro_sem
    if erro_sem:
        if (stage,pos_stage) in erro_sem:
            erro_sem = None
    if erro_sem is None:
        for ret in _sem_analize(action,token,tabela,scopo,log_sem):
            if ret is limpa_last_erro:
                erros_semantico.pop()
            elif ret is not None:
                print(ret,file=log_sem)
                erros_semantico.append(ret)
                if 'erro' in action['s']:
                    erro_sem = action['s']['erro']
    if 'programado' in tabela:
        if tabela['programado'][-1]['when'] == (stage,pos_stage):
            for func,args in tabela['programado'].pop()['do']:
                ret = func(**args)
                if ret is not None:
                    print(ret,file=log_sem)
                    erros_semantico.append(ret)
            if len(tabela['programado']) == 0:
                del(tabela['programado'])


def _sem_analize(action,token,tabela,scopo,log_sem):
    if "s" in action:
        for controle in action['s']['do']:
            yield _sem(controle, token, tabela,scopo,log_sem,action)

import json
class limpa_last_erro():
    pass

def remove_circular_refs(ob, _seen=None):
    if _seen is None:
        _seen = set()
    if id(ob) in _seen:
        return None
    _seen.add(id(ob))
    res = ob
    if isinstance(ob, dict):
        res = {
            remove_circular_refs(key, _seen): remove_circular_refs(value, _seen)
            for key, value in ob.items()}
    elif isinstance(ob, (list, tuple, set, frozenset)):
        res = type(ob)(remove_circular_refs(v, _seen) for v in ob)
    _seen.remove(id(ob))
    return res

def log(func):
    def warp(controle:int, token:dict, tabela:dict,scopo:list[str],log_sem,action):
        print('-> '+controle,scopo,token,erro_sem,file = log_sem,sep=' | ')
        r = func(controle, token, tabela,scopo,log_sem)
        try:
            print(' data:'+json.dumps(remove_circular_refs(tabela['global']),indent=4).replace('\n','\n ')," stack:"+json.dumps(tabela['stack'],indent=4).replace('\n','\n '),sep='\n',file = log_sem)
        except ValueError:
            print(' Data nao pode ser representado pois ele contem loop de referencia.\n'," stack:"+json.dumps(tabela['stack'],indent=4).replace('\n','\n '),sep='\n',file = log_sem)
        return r
    return warp

@log
def _sem(controle:int, token:dict, tabela:dict,scopo:list[str],log_sem):
    match controle:
        case 'append_stack':
            # stack: ...
            tabela['stack'].append(token["token"])
            # stack: ..., tipo
        case 'insert_const_or_var':
            a = _get_scopo(tabela,scopo)
            from analizador_lexico import PRE
            if token["token"] in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE:
                # print(f'retorno {controle} - 2',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type":tabela['stack'][-1],'is_instanciado':False,'is_vetor':False,'is_const':False}
            tabela['stack'].append(token["token"])
            # stack: ..., tipo, var
            tabela['stack'].append(controle)
            # stack: ..., tipo, var, controle
        case "set_const":
            a = _get_scopo(tabela,scopo)
            a[token['token']]["is_const"] = True
        case "atr_const":
            # stack: ..., tipo, var, controle
            tabela['stack'].pop()
            # stack: ..., tipo, var
            var = tabela['stack'].pop()
            # stack: ..., tipo
            tipo = tabela['stack'][-1]
            match tipo:
                case 'string':
                    if token["type"] != 'CAC':
                        # print(f'retorno {controle} - 1',file = log_sem)
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'boolean':
                    if token["token"] not in BOOL:
                        # print(f'retorno {controle} - 2',file = log_sem)
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'real':
                    if token["type"] != 'NRO' and '.' not in token["token"]:
                        # print(f'retorno {controle} - 3',file = log_sem)
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'int':
                    if token["type"] != 'NRO' and '.' in token["token"]:
                        # print(f'retorno {controle} - 4',file = log_sem)
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
            a = _get_scopo(tabela,scopo)
            a[var]['is_instanciado'] = True
        case 'validate_is_vector':
            t = tabela['stack'].pop()
            var = tabela['stack'][-1]
            if(t == "insert_const_or_var"):
                a = _get_in_scopo(var, tabela,scopo)
                if var not in a:
                    # print(f'retorno {controle} - 1',file = log_sem)
                    return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                a[var]["is_vetor"] = True
            else:
                a = _get_in_scopo(var, tabela,scopo)
                if var not in a:
                    # print(f'retorno {controle} - 1',file = log_sem)
                    return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                if not a[var]["is_vetor"]:
                    return f"Na linha {token['line']}, tentando acessar vetor porém {var} não é vetor"
        case 'validate_dimention_acess':
            var = token['token']
            match token['type']:
                case 'IDE':
                    a = _get_in_scopo(var, tabela,scopo)
                    if var not in a:
                        # print(f'retorno {controle} - 1',file = log_sem)
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                    if a[var]['type'] != 'int':
                        # print(f'retorno {controle} - 2',file = log_sem)
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não é interio ( {a[var]['type']} )"
                case 'NRO':
                    if '.' in token["token"]:
                        # print(f'retorno {controle} - 3',file = log_sem)
                        return f"Na linha {token['line']}, tentando realizar acesso em vetor com valor float ( {var} )"
        case 'dec_class':  
            a = _get_scopo(tabela,scopo)
            from analizador_lexico import PRE
            if token["token"] in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                a[token['token']] = {"type":'class',"data":{}}
                tabela['stack'].append(token["token"])
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE and token['token'] != 'main':
                # print(f'retorno {controle} - 2',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type":'class',"data":{}}
            # print(tabela['stack'],file = log_sem)
            tabela['stack'].append(token["token"])
            # print(tabela['stack'],file = log_sem)
        case 'extends_class':
            a = _get_scopo(tabela,scopo)
            if token['token'] not in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, tentou extender a classe {token['token']}, porém esta não foi declarado"
            if a[token['token']]['type'] != "class":
                # print(f'retorno {controle} - 2',file = log_sem)
                return f"Na linha {token['line']}, tentou extender {token['token']}, porém este não é uma classe"
            var = tabela['stack'][-1]
            a[var]['data'] = a[token['token']]['data']
        case 'append_stack_class':
            #scopo: ...
            scopo.append(tabela['stack'][-1])
            #scopo: ...,class_name
            scopo.append('data')
            #scopo: ...,class_name, data
        case 'verify_type_class':
            a = tabela['global']
            if token["token"] not in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, classe {token['token']} não foi encontrada"
            else:
                if a[token['token']]["type"] != 'class':
                    return f"Na linha {token['line']}, {token['token']} foi usado como classe porem é {a[token['token']]['type']}"
            #stack: ...
            tabela['stack'].append(token["token"])
            #stack: ..., type_object
        case 'insert_object':
            a = _get_scopo(tabela,scopo)
            from analizador_lexico import PRE
            if token["token"] in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE:
                # print(f'retorno {controle} - 2',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            # stack: ..., class, data
            a[token['token']] = {"type":tabela['stack'][-1],"data":tabela['global'][tabela['stack'][-1]]['data']}
        case 'pop_stack':
            # stack: ..., _
            tabela['stack'].pop()
            # stack: ...
        case 'clear_stack':
            # stack: ...
            tabela['stack'] = []
            # stack: 
        case 'mov_to_global_scopo':
            while len(scopo)>1:
                scopo.pop()
        case 'creat_func':
            # stack: ..., tipo
            tipo = tabela['stack'].pop()
            # stack: ...
            a = _get_scopo(tabela,scopo)
            from analizador_lexico import PRE
            if token["token"] in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                a[token['token']] = {"type":tipo,'param':{}}
                scopo.append(token["token"])
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE and token['token'] != "main":
                # print(f'retorno {controle} - 2',file = log_sem)
                a[token['token']] = {"type":tipo,'param':{}}
                scopo.append(token["token"])
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type":tipo,'param':{}}
            # scopo: ...            
            scopo.append(token["token"])
            # scopo: ..., func
            # # stack: ...
            # tabela['stack'].append(token["token"])
            # # stack: ..., func
        case 'move_param':
            # scopo: ..., func
            scopo.append("param")
            # scopo: ..., func, param
        case 'change_scopo_to_data':
            # scopo: ..., func, param
            scopo.pop()
            # scopo: ..., func
            a = _get_scopo(tabela,scopo)
            a['data'] = copy.deepcopy(a['param'])
            scopo.append("data")
            # scopo: ..., func, data
        case 'return_func_data':
            # scopo: ..., func, data
            scopo.pop()
            # scopo: ..., func
            a = _get_scopo(tabela,scopo)
            # del(a['data'])
            tabela['stack'].append(scopo.pop())
            # scopo: ...
            # stack: ...,func
        case 'validate_return':
            # stack: ...,func, ??
            tabela['stack'].pop()
            func = tabela['stack'].pop()
            # stack: ...,
            a = _get_scopo(tabela,scopo)
            tipo = a[func]['type']
            if token['type'] == 'IDE': # se retorno ide
                scopo_var = a[func]['data']
                if token["token"] not in scopo_var:
                            return f"Na linha {token['line']}, no retorno da função {func} tentou retorna {token['token']}, porém este nao existe no scopo"
                else:
                    if scopo_var[token['token']]['type'] != tipo:
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {scopo_var[token['token']]['type']}"
            else:
                match tipo:
                    case 'string':
                        if token["type"] != 'CAC':
                            # print(f'retorno {controle} - 1',file = log_sem)
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}"
                    case 'boolean':
                        if token["token"] not in BOOL:
                            # print(f'retorno {controle} - 2',file = log_sem)
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}"
                    case 'real':
                        if token["type"] != 'NRO' and '.' not in token["token"]:
                            # print(f'retorno {controle} - 3',file = log_sem)
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}"
                    case 'int':
                        if token["type"] != 'NRO' and '.' in token["token"]:
                            # print(f'retorno {controle} - 4',file = log_sem)
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}"
                    case 'void':
                        return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}"    
                    case _:
                        a = _get_in_scopo(token['token'],tabela,scopo+[func,'data'])
                        if token['token'] not in a:
                            return f"Na linha {token['line']}, tentou retorna {token['token']}, porem não existe no scopo"
                        elif a[token['token']]['type'] != a[func]['type']:
                            return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}, porém é {token['token']}, do tipo {a[token['token']]['type']}"  
        case "validate_return_void":
            # stack: ...,func
            func = tabela['stack'].pop()
            # stack: ...,
            a = _get_scopo(tabela,scopo)
            if a[func]['type'] != 'void':
                return f"Na linha {token['line']}, retorno da função {func} não foi encontrado"                  
        case 'dec_param_type':
            #stack: ...
            tabela['stack'].append(token['token'])
            #stack: ...,TYPE
        case 'dec_param_IDE':
            if token['token'] in tabela['global']:
                if tabela['global'][token['token']]['type'] != 'class':
                    return f"Na linha {token['line']}, tipo de parametro {token['token']} nao é classe, portanto não pode ser tipo de variavel"
            else:
                return f"Na linha {token['line']}, tipo de parametro {token['token']} não foi encontrado"  
            #stack: ...
            tabela['stack'].append(token['token'])
            #stack: ...,TYPE-IDE
        case 'dec_param':
            #stack: ...,TYPE-?
            tipo = tabela['stack'].pop()
            #stack: ...
            # verifica se ja foi declarado esse parametro
            a = _get_scopo(tabela,scopo)
            if token['token'] in a:
                return f"Na linha {token['line']}, parametro {token['token']} foi declarado novamente"  
            a[token['token']] = {'type':tipo,
                         "is_instanciado": False,
                         "is_vetor": False,
                         "is_const": False
                     }
        case "validade_IDE":
            var = token['token']
            a = _get_in_scopo(var, tabela,scopo)
            if var not in a:
                return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"  
            #stack: ...,
            tabela['stack'].append(var)
            #stack: ..., var
        case 'add_void_stack':
            #stack: ...,
            tabela['stack'].append('void')
            #stack: ..., var
        case 'validate_last_object':
            ide = tabela['stack'][-1]
            a = _get_in_scopo(var, tabela,scopo)
            if a[ide]['type'] in TYPES:
                return f"Na linha {token['line']}, variavel {ide} foi acessada como objeto, porém é {a[ide]['type']}" 
        case 'atribuição':
            #stack: ...,ide
            if 'programado' not in tabela:
                tabela['programado'] = []
            ide = tabela['stack'].pop()
            a = _get_in_scopo(ide, tabela,scopo)
            tabela['programado'].append({'when':(';',0),'do':[
                                                         (validate_same_type_with_stack_last,
                                                            {
                                                                "type":tabela['stack'].pop(),
                                                                'tabela': tabela,
                                                                'process':lambda _,y,z: z.replace('\%\%',y),
                                                                "erro_msg":f"Na linha {token['line']}, tentativa de atribuir \%\% a {ide} que é do tipo {a[ide]['type']}",
                                                            }
                                                         )
                                                        ]
                                    }
                                )
            #stack: ...
        case 'duble_art':
            #stack: ...,ide
            ide = tabela['stack'].pop()
            a = _get_in_scopo(var, tabela,scopo)
            if a[ide]['type'] not in ['int', 'real']:
                return f"Na linha {token['line']}, tentativa de {token['token']}, na varialvel {ide}, porém esta é {a[ide]['type']}" 
        case 'validade_is_str':
            var = token['token']
            a = _get_in_scopo(var, tabela,scopo)
            if var not in a:
                # if var not in _get_scopo(tabela,scopo[:-2]):
                    return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"  
                # else:
                #     tabela['force_next'].append({'is':('object_access',0),
                #                                  'erro_msg':f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"  
                #                             }
                #                         )

            if a[var]['type'] != 'string':
                return f"Na linha {token['line']}, tentativa de carregar string em {var} porém esta é {a[var]['type']}"
            tabela['stack'].append(var)
            tabela['stack'].append(controle)
        case 'stack_NRO':
            if '.' in token['token']:
                tabela['stack'].append('real')
            else:
                tabela['stack'].append('int')
        case 'stack_CAC':
                tabela['stack'].append('string')
        case 'stack_BOOL':
                tabela['stack'].append('boolean')
        case 'valid_method_acess':
            var = tabela['stack'].pop()
            a =  _get_scopo(tabela,scopo[:-2])
            if var not in a:
                return
            tabela['stack'].append(a[var]['type'])
            return limpa_last_erro()
        case 'validade_is_interger':
            if token['type'] == 'NRO':
                if '.' in token['token']:
                    return f"Na linha {token['line']}, posição de acesso a vetor invalida: {token['token']}, deve ser int porém é float"
            else:
                var = token['token']
                a = _get_in_scopo(var, tabela,scopo)
                if var not in a:
                    return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"
                if a[var]['type'] != 'int':
                    return f"Na linha {token['line']}, usando variavel {token['token']} porém esta é não é int, sendo do tipo {a[var]['type']}"
        case 'valid_atribut_acess':#  validar
            var = tabela['stack'].pop()
            a =  _get_scopo(tabela,scopo[:-2])
            if var not in a:
                return
            tabela['stack'].append(a[var]['type'])
            return limpa_last_erro()
        case _:
            pass

# revisar return

def duble_pop(scopo):
    #scopo: ...,func_name,'data'
    scopo.pop()
    #scopo: ...,func_name
    scopo.pop()
    #scopo: ...

def validate_same_type_with_stack_last(type:str,tabela,erro_msg:str,on_success:callable=None,process:str=None):
    _type = tabela['stack'].pop()
    if type != _type:
        if process:
            erro_msg = process(type, _type,erro_msg)
        return erro_msg
    if on_success:
        on_success()

def _get_in_scopo(var, tabela,scopo:list):
    a = tabela #testa
    t = copy.deepcopy(scopo)
    while len(t) >=3:
        for s in t:
            a = a[s]
            if var in a:
                return a
        t=t[:-2]
    if var not in a:
        a = tabela['global']
    return a

def _get_scopo(tabela,scopo):
    a = tabela
    for s in scopo:
        a = a[s]
    return a
