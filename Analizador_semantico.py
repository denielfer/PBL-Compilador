import copy

def init():
    global tabela,scopo, erro_sem, erros_semantico
    tabela = {'global':{}, 'stack':[],'last_scopo':[],'scopo':[]}
    scopo = ["global"]
    erro_sem = None
    erros_semantico = []

from Analizador_sintatico import TYPE, TYPES, ART, ART_DOUBLE, REL, LOG, BOOL

def analize(stage, pos_stage, action, token, log_sem= None):
    if not log_sem: # se for None
        from sys import stdout
        log_sem = stdout
    global erro_sem
    if erro_sem:
        if (stage, pos_stage) in erro_sem:
            erro_sem = None
            print('Analizador semantico re-avatido por chega em :',(stage, pos_stage),file=log_sem)
    # try:
    print(erro_sem,erro_sem is None, )
    if erro_sem is None:
        for ret in _sem_analize(action, token, tabela, scopo, log_sem,(stage, pos_stage)):
            # if ret is limpa_last_erro:
            #     erros_semantico.pop()
            # elif ret is not None:
            if ret is not None and (type(ret) != list or ret[0] != '[') :
                print(ret, file=log_sem)
                erros_semantico.append(ret)
                if 'erro' in action['s']:
                    print('Analizador semantico desatido por erro semantico',(stage, pos_stage),file=log_sem)
                    erro_sem = action['s']['erro']
                    break
        if 'programado' in tabela:
            d = []
            for programado in tabela['programado']:
                if programado['when'] == (stage, pos_stage):
                    print(f"Programado triggered: {programado['when']} -> {programado['log_rep']}",scopo, file=log_sem)
                    d.append(programado)
                    # print(programado,file=log_sem)
                    # print(' data:' + json.dumps(remove_circular_refs(tabela['global']), indent=4).replace('\n', '\n '), " stack:" + json.dumps(tabela['stack'], indent=4).replace('\n', '\n '), " last_scopo:" + json.dumps(tabela['last_scopo'], indent=4).replace('\n', '\n '), sep='\n', file=log_sem)
                    for func,args in programado['do']:
                        ret = func(**args)
                        if ret is not None:
                            print(ret, file=log_sem)
                            erros_semantico.append(ret)
                        # print(" stack:" + json.dumps(tabela['stack'], indent=4).replace('\n', '\n '), f' {scopo}', sep='\n', file=log_sem)
            for p in d:
                tabela['programado'].remove(p)
            if len(tabela['programado']) == 0:
                del(tabela['programado'])
    else:
        print(f'skiped {(stage, pos_stage)}, {token}')
    # except Exception as e:
    #     import traceback
    #     erro_sem = []
    #     erros_semantico.append('Erro irrecuperavel')
    #     print('\n\n',traceback.format_exc(),file=log_sem)

def _sem_analize(action, token, tabela, scopo, log_sem,stg_pos):
    if "s" in action:
        for controle in action['s']['do']:
            yield _sem(controle, token, tabela, scopo, log_sem, action,stg_pos)

import json
# class limpa_last_erro():
#     pass

def remove_circular_refs(ob, _seen=None): ### NAO FOI EU QUE FIZ, PEQUEI E ESQUECI DE ONDE
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
    def warp(controle:int, token:dict, tabela:dict, scopo:list[str], log_sem, action,stg_pos):
        print('-> ' + controle, scopo, token, erro_sem, stg_pos,action, file = log_sem, sep=' | ')
        r = func(controle, token, tabela, scopo, log_sem)
        try:
            # print(' data:' + json.dumps(remove_circular_refs(tabela['global']), indent=4).replace('\n', '\n '), " stack:" + json.dumps(tabela['stack'], indent=4).replace('\n', '\n '), " last_scopo:" + json.dumps(tabela['last_scopo'], indent=4).replace('\n', '\n '), sep='\n', file=log_sem)
            print(" stack:" + json.dumps(tabela['stack'], indent=4).replace('\n', '\n '), " last_scopo:" + json.dumps(tabela['last_scopo'], indent=4).replace('\n', '\n '), " scopo"+ json.dumps(tabela['scopo'], indent=4).replace('\n', '\n '), sep='\n', file=log_sem)
            # print(" stack:" + json.dumps(tabela['stack'][-10:], indent=4).replace('\n', '\n '), " last_scopo:" + json.dumps(tabela['last_scopo'], indent=4).replace('\n', '\n '), sep='\n', file=log_sem)
        except ValueError:
            print(' Data nao pode ser representado pois ele contem loop de referencia.\n', " stack:" + json.dumps(tabela['stack'], indent=4).replace('\n', '\n '), sep='\n', file=log_sem)
        return r
    return warp

@log
def _sem(controle:int, token:dict, tabela:dict, scopo:list[str], log_sem):
    match controle:
        case 'append_stack':
            # stack: ...
            tabela['stack'].append(token["token"])
            # stack: ..., tipo
        case 'insert_const_or_var':
            a = _get_scopo(tabela, scopo)
            from Analizador_lexico import PRE
            if token["token"] in a:
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE:
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type":tabela['stack'][-1], 'is_vetor':False, 'is_const':False}
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
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'boolean':
                    if token["token"] not in BOOL:
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'real':
                    if token["type"] != 'NRO' or '.' not in token["token"]:
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
                case 'int':
                    if token["type"] != 'NRO' or '.' in token["token"]:
                        return f"Na linha {token['line']}, tentando salvar {token['token']} na variavel {var} do tipo {tipo}"
            a = _get_scopo(tabela, scopo)
        case 'validate_is_vector':
            t = tabela['stack'].pop()
            var = tabela['stack'][-1]
            if(t in {"insert_const_or_var", "insert_object"}):
                a = _get_in_scopo(var, tabela, scopo)
                if var not in a:
                    return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                a[var]["is_vetor"] = True
            else:
                try:
                    a = _get_in_scopo(var, tabela, scopo)
                    if var not in a:
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                    if not a[var]["is_vetor"]:
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não é vetor"
                except KeyError:
                    return f"Na linha {token['line']}, tentando acessar vetor porém {var} não é vetor"
        case 'validate_dimention_acess':
            var = token['token']
            match token['type']:
                case 'IDE':
                    a = _get_in_scopo(var, tabela, scopo)
                    if var not in a:
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não foi encontrado em nenhum escopo"
                    if a[var]['type'] != 'int':
                        return f"Na linha {token['line']}, tentando acessar vetor porém {var} não é interio ( {a[var]['type']} )"
                case 'NRO':
                    if '.' in token["token"]:
                        return f"Na linha {token['line']}, tentando realizar acesso em vetor com valor float ( {var} )"
        case 'dec_class':  
            a = _get_scopo(tabela, scopo)
            from Analizador_lexico import PRE
            if token["token"] in a:
                a[token['token']] = {"type":'class', "data":{}}
                tabela['stack'].append(token["token"])
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE and token['token'] != 'main':
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type":'class', "data":{}}
            tabela['stack'].append(token["token"])
        case 'extends_class':
            a = _get_scopo(tabela, scopo)
            if token['token'] not in a:
                return f"Na linha {token['line']}, tentou extender a classe {token['token']}, porém esta não foi declarado"
            if a[token['token']]['type'] != "class":
                return f"Na linha {token['line']}, tentou extender {token['token']}, porém este não é uma classe"
            var = tabela['stack'][-1]
            a[var]['data'] = copy.deepcopy( a[token['token']]['data'])
        case 'append_stack_class':
            #scopo: ...
            scopo.append(tabela['stack'][-1])
            #scopo: ...,class_name
            scopo.append('data')
            #scopo: ...,class_name, data
        case 'verify_type_class':
            a = tabela['global']
            if token["token"] not in a:
                return f"Na linha {token['line']}, classe {token['token']} não foi encontrada"
            else:
                if a[token['token']]["type"] != 'class':
                    return f"Na linha {token['line']}, {token['token']} foi usado como classe porem é {a[token['token']]['type']}"
            #stack: ...
            tabela['stack'].append(token["token"])
            #stack: ..., type_object
        case 'insert_object':
            a = _get_scopo(tabela,scopo)
            from Analizador_lexico import PRE
            if token["token"] in a:
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE:
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            # stack: ..., type_class
            a[token['token']] = {"type":tabela['stack'][-1],
                                 "data":tabela['global'][tabela['stack'][-1]]['data'],
                                 'is_vetor':False,
                                 'is_const':False}
            tabela['stack'].append(token['token'])
            tabela['stack'].append(controle)
            # stack: ..., type_class, controle
        case 'pop_stack':
            # stack: ..., _
            tabela['stack'].pop()
            # stack: ...
        case 'clear_stack':
            # stack: ...
            tabela['stack'] = []
            # stack: 
        case 'mov_to_global_scopo':
            while len(scopo) > 1:
                scopo.pop()
        case 'creat_func':
            # stack: ..., tipo
            tipo = tabela['stack'].pop()
            # stack: ...
            a = _get_scopo(tabela, scopo)
            from Analizador_lexico import PRE
            if token["token"] in a:
                a[token['token']] = {"type": tipo, 'param': {}}
                scopo.append(token["token"])
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE and token['token'] != "main":
                a[token['token']] = {"type": tipo, 'param': {}}
                scopo.append(token["token"])
                return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
            a[token['token']] = {"type": tipo, 'param': {}}
            # scopo: ...            
            scopo.append(token["token"])
            # scopo: ..., func
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
            pass
        case 'validate_return':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': (';', 0), 
                                         'do': [
                                                    (
                                                        val_ret,
                                                        {'tabela':tabela,
                                                         'scopo':scopo,
                                                         'token':token,
                                                         'file':log_sem
                                                        }
                                                    )
                                                ],
                                        'log_rep':'return_prog'
                                    }
                                )
            
        case "validate_return_void":
            if 'programado' in tabela:
                tabela['programado'].clear()
            tabela['last_scopo'].clear()
            # stack: ...,func
            scopo.pop()
            func = scopo.pop()
            # stack: ...,
            a = _get_scopo(tabela, scopo)
            if a[func]['type'] != 'void':
                return f"Na linha {token['line']}, retorno da função {func} não foi encontrado"                  
        case 'dec_param_type':
            #stack: ...
            tabela['stack'].append(token['token'])
            #stack: ...,TYPE
        case 'dec_param_IDE':
            if token['token'] in tabela['global']:
                if tabela['global'][token['token']]['type'] != 'class':
                    return f"Na linha {token['line']}, tipo de parametro {token['token']} não é classe, portanto não pode ser tipo de variavel"
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
            a = _get_scopo(tabela, scopo)
            if token['token'] in a:
                return f"Na linha {token['line']}, parametro {token['token']} foi declarado novamente"  
            a[token['token']] = {'type':tipo,
                         "is_vetor": False,
                         "is_const": False
                     }
        case "validate_IDE":
            var = token['token']
            a = _get_in_scopo(var, tabela, scopo)
            if var == 'this':
                tabela['stack'].append(str(False))
                tabela['stack'].append(scopo[1])
                tabela['stack'].append(var)
            else:
                if var not in a:
                    return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"  
                #stack: ...,
                tabela['stack'].append(str('param' in a[var]))
                tabela['stack'].append(a[var]['type'])
                tabela['stack'].append(var)
                #stack: ..., var
        case 'add_void_stack':
            #stack: ...,
            tabela['stack'].append('void')
            #stack: ..., var
        # case 'validate_last_object':
        #     ide = tabela['stack'][-2]
        #     a = _get_in_scopo(ide, tabela, scopo)
        #     if a[ide]['type'] in TYPES:
        #         return f"Na linha {token['line']}, variavel {ide} foi acessada como objeto, porém é {a[ide]['type']}" 
        #     if tabela['last_scopo'] == []:
        #         tabela['last_scopo'] = copy.deepcopy(scopo)
        #     if tabela['stack'][-1] == 'class':
        #         scopo.clear()
        #         scopo.append('global')
        #     else:
        #         _scopo = _get_scopo_of(ide, tabela, scopo)#,log_sem)
        #         scopo.clear()
        #         for s in _scopo:
        #             scopo.append(s)
        #     scopo.append(ide)
        #     scopo.append('data')
            
        case 'validate_last_object':
            ide = tabela['stack'][-2]
            if ide != 'this':
                a = _get_in_scopo(ide, tabela, scopo)
                if a[ide]['type'] in TYPES:
                    return f"Na linha {token['line']}, variavel {ide} foi acessada como objeto, porém é {a[ide]['type']}" 
                if tabela['last_scopo'] == []:
                    tabela['last_scopo'] = copy.deepcopy(scopo)
                if tabela['stack'][-3] == 'class':
                    scopo.clear()
                    scopo.append('global')
                else:
                    _scopo = _get_scopo_of(ide, tabela, scopo)#,log_sem)
                    scopo.clear()
                    for s in _scopo:
                        scopo.append(s)
                scopo.append(ide)
                scopo.append('data')
            else:
                if tabela['last_scopo'] == []:
                    tabela['last_scopo'] = copy.deepcopy(scopo)
                scopo.clear()
                scopo.append('global')
                scopo.append(tabela['stack'][-3])
                scopo.append('data')
                tabela['stack'].append(tabela['stack'][-3])
        case 'atribuição':
            try:
                if tabela['stack'][-4] == 'True':
                    return f"Na linha {token['line']}, tentativa de atribuir valor a função, {tabela['stack'][-2]}"
            except:
                pass
            #stack: ...,ide
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': (';', 0), 
                                         'do': [
                                                    (validate_same_type_with_stack_last,
                                                    {
                                                        "type":tabela['stack'][-1],
                                                        'tabela': tabela,
                                                        'process':lambda _, y, z: z.replace('\%\%', y),
                                                        "erro_msg":f"Na linha {token['line']}, tentativa de atribuir \%\% em {tabela['stack'][-2]} que é do tipo {tabela['stack'][-1]}",
                                                        'file':log_sem
                                                    }
                                                    )
                                                ],
                                        'log_rep':'Atribuição_prog'
                                    }
                                )
            #stack: ...
        case 'duble_art':
            #stack: ...,ide
            tipo = tabela['stack'][-1]
            if tipo not in ['int', 'real']:
                return f"Na linha {token['line']}, tentativa de {token['token']}, em variavel do tipo {tipo}" 
        case 'schedule_valid_type':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': (';', 0), 
                                         'do': [
                                            (validate_last_in_types,
                                            {
                                                'tabela': tabela,
                                                "erro_msg":f"Na linha {token['line']}, a função read so é aceito int, real, boolean, string ou void",
                                            }
                                            )
                                        ],
                                        'log_rep':'Valid_type_prog'
                                    }
                                )
        case 'schadule_move_back_scopo':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':(';', 0), 
                                         'do':[
                                            (change_back_scopo,
                                            {
                                                '_scopo':copy.deepcopy(scopo),
                                                'scopo':scopo
                                            }
                                            )
                                        ],
                                        'log_rep':'Move_back_scopo_prog'
                                    }
                                )
        case 'schadule_clean_last_scopo':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':(';', 0), 
                                         'do':[
                                            (change_back_scopo,
                                            {
                                                '_scopo':[],
                                                'scopo':tabela['last_scopo']
                                            }
                                            )
                                        ],
                                        'log_rep':'Clean_last_scopo_prog'
                                    }
                                )
        case 'save_scopo':
            if tabela['last_scopo'] == []:
                tabela['last_scopo'] = copy.deepcopy(scopo)  # scopo: ..., class, 'data', method, 'data'
        case 'stack_NRO':
            if '.' in token['token']:
                tabela['stack'].append('real')
            else:
                tabela['stack'].append('int')
        case 'stack_CAC':
                tabela['stack'].append('string')
        case 'stack_BOOL':
                tabela['stack'].append('boolean')
        case 'validate_is_interger':
            if token['type'] == 'NRO':
                if '.' in token['token']:
                    return f"Na linha {token['line']}, posição de acesso a vetor invalida: {token['token']}, deve ser int porém é float"
            else:
                var = token['token']
                a = _get_in_scopo(var, tabela, scopo,file=log_sem)
                if var not in a:
                    return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"
                if a[var]['type'] != 'int':
                    return f"Na linha {token['line']}, usando variavel {token['token']} porém esta é não é int, sendo do tipo {a[var]['type']}"
        case 'validate_object':
            if tabela['last_scopo'] == []:
                tabela['last_scopo'] = copy.deepcopy(scopo)  # scopo: ..., class, 'data', method, 'data'
            var = tabela['stack'].pop() 
            tipo = tabela['stack'][-1]
            a = _get_in_scopo(var,tabela,scopo)
            if var != 'this':
                if  a == tabela['global']:
                    return f"Na linha {token['line']}, {var} não é objeto"
                if var in a:
                    if a[var]['type'] in TYPES:
                        return f"Na linha {token['line']}, usando variavel {var} como objeto, porém esta é tipo {a[var]['type']}"
                _scopo = _get_scopo_of(var,tabela,scopo)
                scopo.clear()
                for s in _scopo:
                    scopo.append(s)
                scopo.append(var)
                scopo.append('data')
                # scopo: ..., class, 'data', method, 'data', objeto, 'data'
            else:
                scopo.clear()
                scopo.append('global')
                scopo.append(tipo)
                scopo.append('data')

        case 'move_scopo_back':
            if tabela['last_scopo'] != []:
                while len(scopo) != 0:
                    scopo.pop()
                for a in tabela['last_scopo']:
                    scopo.append(a)
                tabela['last_scopo'] = []
        case 'validate_atr':
            a = _get_scopo(tabela, scopo)
            if token['token'] not in a:
                return f"Na linha {token['line']}, {token['token']} não foi encontrado como atributo do objeto {scopo[-2]}"
            tabela['stack'].append(str( 'param' in a[token['token']]))
            tabela['stack'].append(token['token'])
            tabela['stack'].append(token['token'])
        case 'acess_method':
            a = _get_scopo(tabela, scopo)
            print(tabela['stack'][-10:],file=log_sem)
            if token['token'] not in a:
                if tabela['last_scopo'] != []:
                    scopo.clear()
                    for a in tabela['last_scopo']:
                        scopo.append(a)
                    tabela['last_scopo'].clear()
                return f"Na linha {token['line']}, {token['token']} não foi encontrado como metodo do objeto da classe {tabela['stack'][-2]}"
            scopo.append(token['token'])
            scopo.append('param')
            # scopo: ..., class, 'data', method, 'data', objeto, 'data', func, 'param'
            tabela['stack'].append('0') # -1 indicando que esperamos o primerio parametro da função
        case 'schedule_add_type_func':
            a = _get_scopo(tabela, scopo[:-1])
            tipo = a['type'] if 'type' in a else 'desconhecido'
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('close_parentesis',0), 
                                         'do':[
                                            (lambda :tabela['stack'].append(tipo),
                                            {}
                                            )
                                        ],
                                        'log_rep':'add_func_type_stack_prog'
                                    }
                                )
        case 'dimention_swap_scopo':
            tabela['scopo'].append(copy.deepcopy(scopo))
            scopo.clear()
            for s in tabela['last_scopo']:
                scopo.append(s)
        case 'dimention_swap_back_scopo':
            _scopo = tabela['scopo'].pop()
            scopo.clear()
            for s in _scopo:
                scopo.append(s)
        case 'add_scopo_func_call':
            tabela['scopo'].append(copy.deepcopy(scopo))
            scopo.clear()
            for a in tabela['last_scopo']:
                scopo.append(a)
            tabela['scopo'].append(copy.deepcopy(tabela['last_scopo']))
            tabela['last_scopo'].clear()
        case 'swap_scopo':
            _scopo = tabela['scopo'].pop()
            tabela['scopo'].append(copy.deepcopy(scopo))
            scopo.clear()
            for a in _scopo:
                scopo.append(a)
        case 'schedule_pop_scopo':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('close_parentesis',0), 
                                         'do':[
                                            (temp,
                                            {}
                                            )
                                        ],
                                        'log_rep':'func_scopo_pop_prog'
                                    }
                                )
        case 'schedule_change_back_scopo':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':(';', 0), 
                                         'do': [
                                            (change_back_scopo,
                                            {
                                                '_scopo':copy.deepcopy(tabela['last_scopo']),
                                                'scopo':scopo
                                            }
                                            )
                                        ],
                                        'log_rep':'change_back_scopo_prog'
                                    }
                                )
            tabela['last_scopo'] = []
        case 'stack_bool':
            tabela['stack'].append('boolean')
        case 'schedule_validate_qtd_param':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('close_parentesis',0), 
                                         'do':[
                                            (valid_qtd_param,
                                            {
                                                'tabela': tabela,
                                                'qtd_param_req':len(_get_scopo(tabela,scopo))-1,
                                                "msg":f"Na linha {token['line']}, quantidade de parametros não conferem, 99 foram fornecidos porém 00 são nescessarios"
                                            }
                                            )
                                        ],
                                        'log_rep':'validate_qtd_param_prog'
                                    }
                    )
        case 'validate_param':
            a = _get_scopo(tabela,scopo)
            index = int(tabela['stack'][-2])
            tipo = tabela['stack'][-1]
            try:
                _tipo = list(a.values())[index]['type']
            except IndexError:
                return f"Na linha {token['line']}, foi dado um {index+1} parametro para função {scopo[-2]}"
            if ( _tipo != tipo):
                return f"Na linha {token['line']}, o parametro {index+1} da função {scopo[-2]} é do tipo {tipo}, e deveria ser {_tipo}"
        case 'schedule_validate_param':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('val_param',0), 
                                         'do':[
                                            (
                                                val_param,
                                                {
                                                    'tabela': tabela,
                                                    'scopo': scopo,
                                                    "token":token,
                                                    'file':log_sem
                                                }
                                            )
                                        ],
                                        'log_rep':'validate_param_prog'
                                    }
                    )
        case 'move_next_param':
            a = -1
            while a > - len(tabela['stack']): # procura o ultimo numero, concerteza tem 0
                if tabela['stack'][a].isdigit():
                    a = tabela['stack'][a]
                    break
                a -= 1
            a = int(a)
            if a < 0:
                raise Exception('nenhum parametro foi declarado antes')
            tabela['stack'].append(str(a+1))
        case 'constructor':
            a = _get_scopo(tabela, scopo)   
            a[token['token']] = {"type": scopo[-2], 'param': {}}
            scopo.append(token["token"])
        case 'validate_last_bool':
            if tabela['stack'][-1] != 'boolean':
                tabela['stack'].append('boolean')
                return f"Na linha {token['line']}, {token['token']} deveria ser boolean, mas é {tabela['stack'][-2]}"
        case 'add_last_var_type':
            try:
                var = tabela['stack'][-1]
                a = _get_in_scopo(var,tabela, scopo)
                tabela['stack'].append(a[var]['type'])
            except Exception as e:
                if tabela['stack'][-1] == 'this':
                    tabela['stack'].append(scopo[1])
                # import traceback
                # print('\n\n',traceback.format_exc(),file=log_sem)
                print(' Erro: ',e,file=log_sem)
        case 'match_last':
            tabela['stack'].append('boolean')
            if token['type'] == 'NRO':
                if tabela['stack'][-2] not in ['real',"int"]:
                    return f"Na linha {token['line']}, {token['token']} deveria ser do tipo {tabela['stack'][-2]}"
            else:
                if tabela['stack'][-2] not in ['string']:
                    return f"Na linha {token['line']}, {token['token']} deveria ser do tipo {tabela['stack'][-2]}"
        case 'schedule_valid_type_on_void':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': ('void',0), 
                                         'do': [
                                            (validate_last_in_types,
                                            {
                                                'tabela': tabela,
                                                "erro_msg":f"Na linha {token['line']}, para operações relacionais é requerido variaveis de tipos basicos (int, real, boolean ou string)",
                                            }
                                            )
                                        ],
                                        'log_rep':'valid_type_on_void_prog'
                                    }
                                )
        case 'schedule_match_type_on_void':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': ('rel_sinc',0), 
                                         'do': [
                                            (validate_type_relacional,
                                            {
                                                'tipo':tabela['stack'][-4], 
                                                'tabela':tabela, 
                                                'erro_msg':f"Na linha {token['line']}, operação relacional com tipo diferentes", 
                                                'file':log_sem
                                            }
                                            )
                                        ],
                                        'log_rep':'match_type_on_void_prog'
                                    }
                                )
        case 'schedule_validate_last_boolean':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': ('void',0), 
                                         'do': [
                                            (validate_last_is_boolean,
                                            {
                                                'tabela': tabela,
                                                "erro_msg":f"Na linha {token['line']}, o que segue '!' deve ser do tipo boolean",
                                            }
                                            )
                                        ],
                                        'log_rep':'validate_last_boolean_prog'
                                    }
                                )
        case 'schadule_change_back_scopo_at_relational':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('relational_expression_value', 0), 
                                        'do':[
                                            (change_back_scopo,
                                             {
                                                '_scopo':tabela['last_scopo'],
                                                'scopo':scopo
                                             }
                                            ),
                                            (clean_last_scopo,{"last_scopo":tabela['last_scopo']})
                                        ],
                                        'log_rep':'Change_back_scopo_at_relational_prog'
                                    }
                                )
        case 'start_vector':
            if tabela['stack'][-1] != '-':
                if tabela['stack'][-1] != '|' and tabela['stack'][-2] != '|':
                    tabela['stack'].append('|')
                elif tabela['stack'][-2] == '|':
                    tabela['stack'].append('-')
        case 'add_type_of_or_validate':
            if tabela['stack'][-2] == '|':
                tabela['stack'].append('-')
            if tabela['stack'][-1] != '-':
                if token['type'] == 'CAC':
                    tabela['stack'].append('string')
                elif token['type'] == 'NRO':
                    if '.' in token['token']:
                        tabela['stack'].append('real')
                    else:
                        tabela['stack'].append('int')
                else:
                    var = token['token']
                    a = _get_in_scopo(var,tabela,scopo)
                    if var not in a:
                        return f"Na linha {token['line']}, {token['token']} não foi declarado"
                    tabela['stack'].append(a[var]["type"])
                tabela['stack'].append('-')
            else:
                if token['type'] == 'CAC':
                    if tabela['stack'][-2] != 'string':
                        return f"Na linha {token['line']}, vetor deve ser do tipo {tabela['stack'][-2]} mas encontrado {token[token]}, do tipo string"
                elif token['type'] == 'NRO':
                    if '.' in token['token']:
                        if tabela['stack'][-2] != 'real':
                            return f"Na linha {token['line']}, vetor deve ser do tipo {tabela['stack'][-2]} mas encontrado {token[token]}, do tipo real"
                    else:
                        if tabela['stack'][-2] != 'int':
                            return f"Na linha {token['line']}, vetor deve ser do tipo {tabela['stack'][-2]} mas encontrado {token[token]}, do tipo int"
                else:
                    var = token['token']
                    a = _get_in_scopo(var,tabela,scopo)
                    if var not in a:
                        return f"Na linha {token['line']}, {token['token']} não foi declarado"                    
                    if tabela['stack'][-2] != a[var]['type']:
                        return f"Na linha {token['line']}, vetor deve ser do tipo {tabela['stack'][-2]} mas encontrado {token[token]}, do tipo {a[var]['type']}"
        case 'vector_end':
            if tabela['stack'][-1] == '-':
                tabela['stack'].pop()
        case 'vector_add_end':
            if tabela['stack'][-1] != '-':
                tabela['stack'].append('-')
        case 'validate_int_or_real':
            if token['type'] == 'NRO':
                if '.' in token['token'] and tabela['stack'][-1] != 'real':
                    return f"Na linha {token['line']}, {token['token']} em operação aritimetica, deveria ser {tabela['stack'][-1]} mas é real"
                elif '.' not in token['token'] and tabela['stack'][-1] != 'int':
                    return f"Na linha {token['line']}, {token['token']} em operação aritimetica, deveria ser {tabela['stack'][-1]} mas é int"
        case 'schedule_match_type_on_arit_expression':
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when': ('arit_expression', 0), 
                                         'do': [
                                            (
                                                validate_type_arit_expression,
                                                {
                                                    'tipo':tabela['stack'][-1], 
                                                    'tabela':tabela, 
                                                    'erro_msg':f"Na linha {token['line']}, operação aritimetica com tipo diferentes", 
                                                }
                                            )
                                        ],
                                        'log_rep':'match_type_on_arit_expression_prog'
                                    }
                                )
        case 'schedule_change_back_scopo_parent':
            return
            if 'programado' not in tabela:
                tabela['programado'] = []
            tabela['programado'].append({'when':('method_access', 2), 
                                         'do': [
                                            (
                                                change_back_scopo,
                                                {
                                                    '_scopo':copy.deepcopy(scopo),
                                                    'scopo':scopo,
                                                    'file':log_sem
                                                }
                                            )
                                        ],
                                        'log_rep':'change_back_scopo_parent_prog'
                                    }
                                )
        case 'validate_is_class':
            if token['token'] not in tabela['global']:
                return f"Na linha {token['line']}, {token['token']} não foi declarado como classe"
        case 'validate_constructor':
            print(tabela['scopo'],file=log_sem)
            if tabela['stack'][-3] != 'class':
                if tabela['last_scopo'] != []:
                    scopo.clear()
                    for s in tabela['last_scopo']:
                        scopo.append(s)
                    tabela['last_scopo'].clear()
                return f"Na linha {token['line']}, tentando chamar construtor de objeto e não class"
        case 'add_NRO_or_CAC':
            if token['type'] == 'CAC':
                tabela['stack'].append('string')
            elif token['type'] == 'NRO':
                if '.' in token['token']:
                    tabela['stack'].append('real')
                else:
                    tabela['stack'].append('int')
        case _:
            pass

def val_param(tabela,scopo,token,file=None):
        # tabela['stack'].pop()
        # print(tabela['scopo'],file=file)
        _scopo = tabela['scopo'][1]
        tabela['scopo'].append(copy.deepcopy(scopo))
        scopo.clear()
        for a in _scopo:
            scopo.append(a)
        # print(scopo,file=file)
        paran = _get_scopo(tabela,scopo)
        # print(paran,file=file)
        c = 0
        while c < len(tabela['stack']):
            c +=1
            try:
                int(tabela['stack'][-c])
            except:
                continue
            break
        # print(tabela['stack'],file=file)
        index = int(tabela['stack'][-c])
        tipo = tabela['stack'][-1]
        _scopo = scopo
        try:
            _tipo = list(paran.values())[index]['type']
        except IndexError:
            return f"Na linha {token['line']}, foi dado um {index+1} parametro para função {scopo[-2]}"
        if ( _tipo != tipo):
            return f"Na linha {token['line']}, o parametro {index+1} da função {_scopo[-2]} é do tipo {tipo}, e deveria ser {_tipo}"
        

def temp():
    _scopo = tabela['scopo'].pop()
    scopo.clear()
    for s in _scopo:
        scopo.append(s)

def val_ret(tabela,scopo,token,file=None):
    tabela['last_scopo'].clear()
    # stack: ...,func, ??
    scopo.pop()
    func = scopo.pop()
    # stack: ...,
    a = _get_scopo(tabela, scopo)
    tipo = a[func]['type']
    _tipe = tabela['stack'][-1]
    print(tabela['stack'][-1:],tipo,file=file)
    if tipo != _tipe:
        return f"Na linha {token['line']}, retorno da função {func} devia ser {tipo}" #, porém é {_tipe}  
            

def clean_last_scopo(last_scopo):
    last_scopo.clear()

def validate_same_type_with_stack_last(type:str, tabela, erro_msg:str, process:str=None,file=None):
    _type = tabela['stack'][-1]
    print(type,_type,file=file)
    if type != _type:
        if process:
            erro_msg = process(type, _type, erro_msg)
        return erro_msg

def validate_last_in_types(tabela, erro_msg:str):
    try:
        tipo= tabela['stack'][-1]
        if tipo not in TYPES :
            return erro_msg
    except :
        return erro_msg

def change_back_scopo(_scopo,scopo,file=None):
    print(_scopo,scopo,file=file)
    if _scopo != []:
        while len(scopo) !=0:
            scopo.pop()
        for a in _scopo:
            scopo.append(a)

def valid_qtd_param(tabela,qtd_param_req, msg:str):
    a = -1
    while a > - len(tabela['stack']): # procura o ultimo numero, concerteza tem 0
        if tabela['stack'][a].isdigit():
            a = tabela['stack'][a]
            break
        a -= 1
    a = int(a)
    if a < 0:
        a = 0
    if qtd_param_req <0:
        qtd_param_req=0
    msg = msg.replace('99', str(a+1)).replace('00', str(qtd_param_req+1))
    if a != qtd_param_req:
        return msg
    
def validate_last_is_boolean(tabela,erro_msg):
    if tabela['stack'][-1] != 'boolean':
        return erro_msg

def validate_type_arit_expression(tipo,tabela,erro_msg):
    tabela['stack'].append(tipo)
    if tabela['stack'][-2] != tipo:
        return erro_msg

def validate_type_relacional(tipo,tabela,erro_msg,file):
    tabela['stack'].append('boolean')
    print(tipo,tabela['stack'][-4:],file=file)
    if tipo in ['real','int']:
        if tabela['stack'][-2] not in ['real','int']:
            return erro_msg
    elif tabela['stack'][-2] != tipo:
        return erro_msg

def _get_scopo_of(var, tabela, scopo:list,file = None):
    t = copy.deepcopy(scopo)
    a = None
    while len(t) > 0:
        a = tabela
        for s in t:
            a = a[s]
        if var in a:
            return t
        t = t[:-2]
    if not a or var not in a:
        return None


def _get_in_scopo(var, tabela, scopo:list,file = None):
    t = copy.deepcopy(scopo)
    a = None
    while len(t) > 0:
        a = tabela
        for s in t:
            a = a[s]
        if var in a:
            return a
        t = t[:-2]
    if not a or var not in a:
        a = tabela['global']
    return a

def _get_scopo(tabela, scopo):
    a = tabela
    for s in scopo:
        a = a[s]
    return a
