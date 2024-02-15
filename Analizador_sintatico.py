
# Tipos
TYPE = ['int', 'real', 'boolean', 'string']

# Tipos com void
TYPES = TYPE + ['void'] # menos IDE
import copy

# Aritméticos simples
ART = {'+', '-', '*', '/'}

# Aritméticos incremento
ART_DOUBLE = {'++', '--'}

# Relacionais
REL =  {'<', '<=', '>', '>=', '!=', '=='}

# Lógicos
LOG = {'&&', '||'}

# Booleanos
BOOL = {'true', 'false'}

# Gramática do Problema 2 ajustada
get_functions = {
    'const': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['const'], 'next': [('const', 1)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('const', 2)]},
                ],'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": TYPE, 'next': [('const', 2), ('const', 3)], 's': {'do': ['append_stack']}},
                    {'is_terminal': True, "key":'token', "value": [''], 'next': []},
                ],'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('const', 4)], 's': {'do': ['insert_const_or_var', 'set_const'], 'erro':[('const', 6)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['='], 'next':[('const', 5)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": BOOL, 'next': [('const', 6)], 's': {'do': ['atr_const']}},
                    {'is_terminal': True, "key": 'type', "value": ['NRO', 'CAC'], 'next': [('const', 6)], 's': {'do': ['atr_const']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [','], 'next': [('const', 3)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [(";", 0)], 's': {'do': ["pop_stack"]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
            ],
    'variables': [
                    {"test": [
                        {'is_terminal': True, "key": 'token', "value": ['variables'], 'next': [('variables', 1)]},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                    {"test": [
                        {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('variables', 2)]},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                    {"test": [
                        {'is_terminal': True, "key": 'token', "value": TYPE, 'next': [('variables', 2), ('variables', 3)], 's': {'do': ['append_stack']}},
                        {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                    {"test": [
                        {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('variables', 4), ('dimention_acess', 0)], 's': {'do': ['insert_const_or_var'], 'erro': [('variables', 4)]}},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                    {"test": [
                        {'is_terminal' :True, "key": 'token', "value": [','], 'next': [('variables', 3)], 's': {'do': ['pop_stack']}},
                        {'is_terminal' :True, "key": 'token', "value": [''], 'next': [(";", 0)]},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                ],
    'class': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['class'], 'next': [('class', 1)], 's': {'do': ['clear_stack', 'mov_to_global_scopo']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ 
                # ('end_block',0) é colocado aqui pois da forma como é feita ao colocar no 4 daria problema com empacotar construtor, precisando de branch para main e classe normal, assim, colocando aqui reduz codigo
                    {'is_terminal': True, "key": 'token', "value": ['main'], 'next': [('end_block', 0), ('class', 5)], 's': {'do': ['dec_class']}},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('class', 0), ('end_block', 0), ('constructor', 0), ('class', 2)], 's': {'do': ['dec_class']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['extends'], 'next': [("class", 3)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [("class", 4)]},
                ] ,'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                  {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [("class", 4)], 's': {'do': ['extends_class']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('methods', 0), ('object', 0), ("variables", 0)], 's': {'do' :['append_stack_class']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('methods', 2), ('object', 0), ("variables", 0)], 's': {'do': ['append_stack_class']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
              ],
    'object': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['objects'], 'next': [('object', 1)]}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('object', 2)]}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('object', 2), ('object', 3)], 's': {'do': ['verify_type_class'], 'erro': [(";", 0)]}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next':[]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('object', 4), ('dimention_acess', 0)], 's': {'do': ['insert_object'], 'erro': [('object', 4)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [','], 'next': [('object', 3)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [(";", 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
            ],
    'methods' :[ 
                {"test": [
                   {'is_terminal': True, "key": 'token', "value": ['methods'], 'next': [('methods', 1)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('func_dec', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ # para main pois precisamos forçar a função main como primeira e ela é diferente
                   {'is_terminal': True,"key": 'token', "value": ['methods'], 'next': [('methods', 3)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('func_dec', 0), ('func_main', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
               ],
    'func_main': [
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": TYPES, 'next': [('func_main', 1)], 's': {'do': ['append_stack']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": ['main'], 'next': [('func_main', 2)], 's': {'do': ['creat_func'], 'erro': [('func_dec', 0)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('func_dec', 3), ("close_parentesis", 0)], 's': {'do': ['move_param']}},
                ], 'erro': {'tipo_recuperação': 'next'}}, # tem move_param pois apesar de nao ter parametro, o proximo ('func_dec',3) começa com scopo.pop()
    ],
    'func_dec': [
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": TYPES, 'next': [('func_dec', 1)], 's': {'do': ['clear_stack','append_stack']}},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('func_dec', 1)], 's': {'do': ['clear_stack','append_stack']}},
                    {'is_terminal': True, "key": 'type', "value": [''], 'next': [], 's': {'do': ['clear_stack']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('func_dec', 0), ('func_dec', 2)], 's': {'do': ['creat_func']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('func_dec', 3), ("close_parentesis", 0), ('dec_parameter', 0)], 's': {'do': ['move_param']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ('return', 0), ("command", 0), ('object', 0), ('variables', 0)], 's': {'do': ['change_scopo_to_data']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'return': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['return'], 'next': [('return', 1)], 's': {'do': ['return_func_data']}}
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': False, 'terminais': [('value', 0)], 'next': [(";", 0)], 's': {'do': ['validate_return']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [(";", 0)], 's': {'do': ['validate_return_void']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
            ],
    'end_block': [ # ("end_block",0),
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['}'], 'next': []}
                ], 'erro': {'tipo_recuperação': 'next'}}
                ],
    'dec_parameter': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": TYPE, 'next': [('dec_parameter', 1)], "s": {'do': ['dec_param_type']}},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('dec_parameter', 1)], "s": {'do': ['dec_param_IDE'], 'erro': [('mult_dec_parameter', 0)]}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('mult_dec_parameter', 0)], 's': {'do': ['dec_param']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'mult_dec_parameter': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [','], 'next': [('mult_dec_parameter', 1)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": TYPE, 'next': [('dec_parameter', 1)], "s": {'do': ['dec_param_type']}},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('dec_parameter', 1)], "s": {'do': ['dec_param_IDE'], 'erro': [('mult_dec_parameter', 0)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'command': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['print'], 'next': [('command', 0), (";", 0), ('print', 0)]},
                    {'is_terminal': True, "key": 'token', "value": ['read'], 'next': [('command', 0), (";", 0), ('read', 0)]},
                    {'is_terminal': True, "key": 'token', "value": ['if'], 'next': [('command', 0), ('if', 0)]},
                    {'is_terminal': True, "key": 'token', "value": ['for'], 'next': [('command', 0), ('for', 0)]},
                    {'is_terminal': True, "key": 'token' , "value": ['this'], 'next': [('command', 0), ("assigment_or_method_acess_or_duble", 1), ('object_access', 0)], 's': {'do': ['validate_IDE', "add_void_stack"], 'erro': [(';', 0), ('command', 0)]}},
                    {'is_terminal': True, "key": 'type' , "value": ['IDE'], 'next': [('command', 0), ('assigment_or_method_acess_or_duble', 0)], 's': {'do': ['validate_IDE', "add_void_stack"], 'erro': [(';', 0), ('command', 0)]}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}}
    ],
    'assigment_or_method_acess_or_duble': [
                {"test": [
                    {'is_terminal': False, 'terminais': [('dimention_acess', 0)], 'next': [("assigment_or_method_acess_or_duble", 1), ('object_access', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['->'], 'next': [(';', 0), ('method_access', 1)], 's': {'do': ['validate_last_object'], 'erro': [(';', 0)]}},
                    {'is_terminal': True, "key": 'token', "value": ['='], 'next': [(';', 0), ('value', 0)], 's': {'do': ['move_scopo_back','atribuição']}},
                    {'is_terminal': True, "key": 'token', "value": ART_DOUBLE, 'next': [(';', 0)], 's': {'do': ['duble_art','move_scopo_back']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'for': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [
                                                                                ("if", 4), # '{' <command> '}'
                                                                                ("close_parentesis", 0),
                                                                                ('var_assinement', 2),
                                                                                ('object_access', 1),
                                                                                (";", 0),
                                                                                ('relational_expression_value', 2),
                                                                                ('relational_expression_value', 1),
                                                                                (";", 0),
                                                                                ('var_assinement', 0),
                                                                            ]},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'var_assinement': [ # TO DO Validar
        # <ASSIGMENT_WITHOUT_SEMICOLON> -> index [0,1]
                {"test": [ # <DEC_OBJECT_ATRIBUTE_ACCESS>
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('var_assinement', 1), ('object_access', 0), ("dimention_acess", 0)], 's': {'do': ['validate_IDE', 'add_void_stack','save_scopo'], 'erro': [(';', 0)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ 
                    {'is_terminal': True, "key": 'token', "value": ['='], 'next': [('value', 0)], 's': {'do': ['move_scopo_back', 'atribuição']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ # <ASSIGNMENT>
                    {'is_terminal': True, "key": 'token', "value": ['='], 'next': [('value', 0)], 's': {'do': ['move_scopo_back', 'atribuição']}},
                    {'is_terminal': True, "key": 'token', "value": ART_DOUBLE, 'next': [], 's': {'do': ['duble_art']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
            ],
    'value': [ # TO DO validar
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['NRO'], 'next': [("arit_expression", 0)], 's': {'do': ['stack_NRO']}}, 
                    {'is_terminal': True, "key": 'type', "value": ['CAC'], 'next': [], 's': {'do': ['stack_CAC']}},
                    {'is_terminal': True, "key": 'token', "value": ['['], 'next': [("vetor_assinement", 0)], 's': {'do': ['start_vector']}},
                    {'is_terminal': True, "key": 'token', "value": ['!'], 'next': [('logical_expression', 1), ('void',0), ('logical_expression', 0)], 's': {'do': ['schedule_validate_last_boolean']}},
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('aritimetic_or_logical_parentesis_expression', 0)]},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('aritimetic_or_logical_expression', 0), ('object_access', 0), ("dimention_acess", 0)], 's': {'do': ['validate_IDE', "add_void_stack", 'save_scopo']}},
                    {'is_terminal': True, "key": 'token', "value": BOOL, 'next': [], 's': {'do': ['stack_BOOL']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'aritimetic_or_logical_parentesis_expression': [
                {"test": [
                    {'is_terminal': False, 'terminais': [('arit_expression', 1)], 'next': [("arit_expression", 0), ("close_parentesis", 0)]},
                    {'is_terminal': False, 'terminais': [('logical_expression', 0)], 'next': [
                                                                                                ("logical_expression", 1),
                                                                                                ("close_parentesis", 0),
                                                                                                ("logical_expression", 1)
                                                                                            ]},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'aritimetic_or_logical_expression': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['->'], 'next': [('logical_expression', 1), ('relational_expression_value', 0), ('method_access', 1)], 's': {'do': ['validate_last_object', "schadule_change_back_scopo_at_relational"], 'erro': [(';', 0)]}},
                    {'is_terminal': True, "key": 'token', "value": ART_DOUBLE, 'next': [], 's': {'do': ['duble_art','move_scopo_back']}},
                    {'is_terminal': True, "key": 'token', "value": ART, 'next': [('arit_expression', 1)], 's': {'do': ['duble_art','move_scopo_back']}},
                    {'is_terminal': False, "terminais": [("relational_expression_value", 2)],'next': [('logical_expression', 1)],'s': {'do':['move_scopo_back']}},
                    {'is_terminal': True, "key": 'token', "value": LOG, 'next': [('logical_expression', 1), ('logical_expression', 0)], 's': {'do':["move_scopo_back"]}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [], 's': {'do': ["move_scopo_back"]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'logical_expression': [ 
        # <LOGICAL_EXPRESSION> -> todos
                {"test": [ # logical_expression_begin
                    {'is_terminal': True, "key": 'token', "value": ['!'], 'next': [('void', 0), ('logical_expression', 0)], 's': {'do': ['schedule_validate_last_boolean']}},
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [("close_parentesis", 0), ('logical_expression', 1), ('logical_expression', 0)]},
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [("relational_expression_value", 0), ('method_access', 0), ('object_access', 0), ("dimention_acess", 0)], 's': {'do': ['validate_IDE', 'add_void_stack']}},
                    {'is_terminal': True, "key": 'token', "value": BOOL, 'next': [], 's': {'do': ['stack_bool']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [# logical_expression_end
                    {'is_terminal': True, "key": 'token', "value": LOG, 'next': [('logical_expression', 1), ('logical_expression', 0)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'relational_expression_value': [
        # index [1,2,1] -> <RELATIONAL_EXPRESSION>
                {"test": [ # <LOG_REL_OPTIONAL>
                    {'is_terminal': True, "key": 'token', "value": REL, 'next': [('relational_expression_value', 1), ('void', 0)], 's': {'do': ['schedule_valid_type_on_void']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ # <RELATIONAL_EXPRESSION_VALUE>
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('void',0),('method_access', 0), ('object_access', 0), ("dimention_acess", 0)], 's': {'do': ['add_void_stack', 'schedule_match_type_on_void']}},
                    {'is_terminal': True, "key": 'type', "value": ['NRO','CAC'], 'next': [], 's': {'do': ['match_last']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ 
                    {'is_terminal': True, "key": 'token', "value": REL, 'next': [('relational_expression_value', 1), ('void', 0)], 's': {'do': ['schedule_valid_type_on_void']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'method_access': [
                {"test": [ # <optional_method_access>
                    {'is_terminal': True, "key": 'token', "value": ['->'], 'next': [('method_access', 1)], 's': {'do': ['validate_last_object'], 'erro': [(';', 0)]}}, 
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [],'s':{'do':['add_last_var_type']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('method_access', 2)], 's': {'do': ['acess_method', "schedule_add_type_func"]}},
                    {'is_terminal': True, "key": 'token', "value": ['constructor'], 'next': [('method_access', 2)], 's': {'do': ['acess_method', 'schedule_add_type_func']}},#to do validar
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('close_parentesis', 0), ("parameters", 0)], 's': {'do': ['schedule_change_back_scopo', 'schedule_validate_qtd_param']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'parameters': [
                {"test": [ #<PARAMETERS>
                    {'is_terminal': False, "terminais": [("value", 0)], 'next': [('parameters', 1)], 's': {"do": ['validate_param']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ # <MULT_PARAMETERS>
                    {'is_terminal': True, "key": 'token', "value": [','], 'next': [('parameters', 1), ('parameters', 2)], 's': {"do": ['move_next_param']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ 
                    {'is_terminal': False, "terminais": [("value", 0)], 'next': [('parameters', 1)], 's': {"do": ['validate_param']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'vetor_assinement': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['['], 'next': [('vetor_assinement', 1), ('vetor_assinement', 0)], 's': {'do': ['start_vector']}},
                    {'is_terminal': True, "key": 'type', "value": ['IDE', 'CAC', 'NRO'], 'next': [('vetor_assinement', 1)], 's': {'do': ['add_type_of_or_validate']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [','], 'next': [('vetor_assinement', 0)], 's': {'do': ['vector_add_end']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [('vetor_assinement', 2)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value" :[']'], 'next': [], 's': {'do': ['vector_end']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'arit_expression': [
                {"test": [ # <END_EXPRESSION_OPTIONAL>
                    {'is_terminal': True, "key": 'token', "value": ART, 'next': [('arit_expression', 1)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ #<SIMPLE_EXPRESSION>
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('arit_expression', 0), ('object_access', 0), ("dimention_acess", 0)],'s':{'do':['schedule_match_type_on_arit_expression','validate_IDE','add_void_stack']}},
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('arit_expression', 0), ('close_parentesis', 0), ('arit_expression', 1)]},
                    {'is_terminal': True, "key": 'type', "value": ['NRO'], 'next': [('arit_expression', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [ # <END_EXPRESSION>
                    {'is_terminal': True, "key": 'token', "value": ART, 'next': [('arit_expression', 1)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'if': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('if', 1), ("close_parentesis", 0), ('logical_expression', 1), ('logical_expression', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['then'], 'next': [('if', 2)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('if', 3), ("end_block", 0), ('command', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['else'], 'next': [('if', 4)]},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [("end_block", 0), ('command', 0)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
    ],
    'read': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [("close_parentesis", 0), ('read', 1)], "s": {'do': ['schadule_move_back_scopo', 'schadule_clean_last_scopo']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('object_access', 0), ("dimention_acess", 0)], "s": {'do': ['schedule_valid_type','validate_IDE','add_void_stack'], 'erro': [("close_parentesis", 0), (';', 0)]}},
                ], 'erro': {'tipo_recuperação': 'next'}}
    ],
    "print": [ 
                {"test" :[
                    {'is_terminal': True, "key": 'token', "value": ['('], 'next': [("close_parentesis", 0), ('print', 1)]},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [('object_access', 0), ("dimention_acess", 0)], 's': {'do': ["validate_IDE", "add_void_stack"], 'erro': [("close_parentesis", 0), (';', 0)]}},
                    {'is_terminal': True, "key": 'type', "value": ['CAC', 'NRO'], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}}
    ],
    "close_parentesis": [ # ("close_parentesis",0),
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [')'], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}}
    ],
    'dimention_acess': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['['], 'next': [("dimention_acess", 1)], 's': {'do': ["validate_is_vector"], 'erro': [("dimention_acess", 2)]}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [], 's': {'do': ["pop_stack"]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE', 'NRO'], 'next': [("dimention_acess", 2)], 's': {'do': ["validate_is_interger"]}},
                ], 'erro': {'tipo_recuperação': 'next'}}, # ,'s':{'do':["validate_dimention_acess"]}
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [']'], 'next': [("dimention_acess", 0)], 's': {'do': ["add_void_stack"]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                # {"test":[
                #     {'is_terminal':True,"key":'token',"value":['['],'next':[("dimention_acess",1)]},
                # ],'erro':{'tipo_recuperação':'next'}},
               ],
    'object_access': [ 
        # <DEC_OBJECT_ATRIBUTE_ACCESS> -> começa do index 1
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['.'], 'next': [("object_access", 1)], 's': {'do': ['validate_object']}},
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': [],'s':{'do':['add_last_var_type']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {"test": [
                    {'is_terminal': True, "key": 'type', "value": ['IDE'], 'next': [("object_access", 0), ("dimention_acess", 0)], 's': {'do': ['validate_atr', 'add_void_stack'], 'erro': [(';', 0)]}},
                ], 'erro': {'tipo_recuperação': 'next'}},
               ],
    ';': [ # (";",0),
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [';'], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
        ],
    'constructor': [
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": ['constructor'], 'next': [("constructor", 1)], 's': {'do': ['constructor']}},
                ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                        {'is_terminal': True, "key": 'token', "value": ['('], 'next': [('constructor', 2), ("close_parentesis", 0), ('dec_parameter', 0)], 's': {'do': ['move_param']}},
                    ], 'erro': {'tipo_recuperação': 'next'}},
                {'test': [
                        {'is_terminal': True, "key": 'token', "value": ['{'], 'next': [('end_block', 0), ("command", 0), ('object', 0), ('variables', 0)], 's': {'do': ['change_scopo_to_data']}},
                    ], 'erro': {'tipo_recuperação': 'next'}},
            ],
    'void': [ # void operation so pra fazer schedule de operação so semantico
                {"test": [
                    {'is_terminal': True, "key": 'token', "value": [''], 'next': []},
                ], 'erro': {'tipo_recuperação': 'next'}},
            ],
}

def recuperação_next(list_actions, stack):
    for item in list_actions[-1]["next"]: # adiciona a pilha a última possibilidade do token
        stack.append(item)

recuperação_de_erros = {
    "next": recuperação_next,
}

import Analizador_semantico

def _get_list_actions(stage:str, pos_stage:int):
    list_actions_return = []
    for ac in get_functions[stage][pos_stage]['test']:
        if ac['is_terminal']:
            # print(f'\t\tis_terminal ->{ac}')
            list_actions_return.append(ac)
        else:
            for nao_terminal in ac['terminais']: 
                # não lida com indeterminação, se tiver 2 caminhos pra IDE vai ir no que aparecer primeiro na lista
                # se tiver '' nas produções do action ele vai ser chamado assim q aparecer na lista lá embaixo, o que gera um problema, 
                # então não é chamado para não-terminais que tenham '' nas produções
                # print(nao_terminal)
                for action_new in _get_list_actions(*nao_terminal):
                    # print(action_new)
                    new_dic = copy.deepcopy(action_new)
                    new_dic['next'] = ac['next'] + action_new['next']
                    if 's' in ac:
                        if 's' not in new_dic:
                            new_dic['s'] = {'do': []}
                        # print(new_dic['s'])
                        new_dic['s']['do'] += ac['s']['do']
                        # print(new_dic['s'])
                        if 'erro' in ac['s']:
                            if 'erro' not in new_dic['s']:
                                new_dic['s']['erro'] = []
                            new_dic['s']['erro'] += ac['s']['erro']
                        # print(new_dic['s'])
                    list_actions_return.append(new_dic)
                    # print(f'\t\tis not terminal -> {new_dic}, -> adicionado {ac["next"]}')
    return list_actions_return

# from _typeshed import SupportsWrite
# def analize(get_token:list,log_sem:SupportsWrite[str]):
def analize(get_token:list, log_sem):
    stack = [('END', 0), ('class', 0), ('variables', 0), ("const", 0)]
    stage = None
    Analizador_semantico.init()
    for token in get_token:
        if token['token'] == 'constructor':
            token['type'] = 'PRE'
        elif token['token'] == 'this':
            token['type'] = 'IDE'
        flag = True # se tiver produção vazia continuamos a análise com o mesmo token
        while flag: # suporte para produção vazia
            stage,pos_stage = stack.pop(-1) # por ser pop em '-1' le a pilha da direita pra esquerda
            print('\t', stage, pos_stage, 'token : ', token, ' |', ' stack :', stack)
            flag = False
            if stage == 'END':
                yield f"Na linha {token['line']}, era esperado 'EOF' porém foi obtido {token['token']}"
                stack.append(('END', 0))
                continue
            list_actions = _get_list_actions(stage, pos_stage)
            esperado = []
            for action in list_actions: # para cada token na lista de tokens esperados
                print(f'\t\tbuscando {action}')
                if token[action['key']] in action["value"]: # verifica se o token é o esperado
                    for item in action["next"]:
                        stack.append(item)
                    Analizador_semantico.analize(stage, pos_stage, action, token, log_sem)
                    #     getattr(semant, get_functions[stage][pos_stage]['s']['do'])(**get_functions[stage][pos_stage]['s']['param'],token = token,scopo=scopo)
                    break
                # pode dar erro se vazio não for o primeiro token
                elif "" in action["value"]: # se for token vazio, continuamos em busca pelo próximo elemento
                    for item in action["next"]:
                        stack.append(item)
                    Analizador_semantico.analize(stage, pos_stage, action, token, log_sem)
                    flag = True
                    break
                else: # se não for o token esperado e não tiver token vazio esperado, adicionamos a lista de esperados
                    esperado += action["value"] 
            else: # se não achou ação para o token é porque é token não esperado
                esperado = str(esperado).replace("'IDE'","IDE").replace("'NRO'","NRO").replace("'CAC'","CAC")
                print(f'\t\t\tNa linha {token["line"]}, era esperado {esperado} porém foi obtido \'{token["token"]}\'')
                if get_functions[stage][pos_stage]['erro']['tipo_recuperação'] in recuperação_de_erros:
                    recuperação_de_erros[get_functions[stage][pos_stage]['erro']['tipo_recuperação']](list_actions,stack)
                else:
                     raise Exception('Recuperação requerida mas não implementada')
                yield f"Na linha {token['line']}, era esperado {esperado} porém foi obtido \'{token['token']}\' "
    else: # quando os tokens acabarem
        for item in stack[::-1]: # para cada item na stack
            stage, pos_stage = item
            if stage != 'END': # se não for o fim gera o erro
                list_actions = get_functions[stage][pos_stage]['test']
                esperado = []
                for action in list_actions:
                    esperado += action["value"] 
                esperado = str(esperado).replace("'IDE'", "IDE").replace("'NRO'", "NRO").replace("'CAC'", "CAC")
                yield f"Na linha {token['line'] + 1}, era esperado {esperado} porém foi obtido 'EOF'"
    return Analizador_semantico.erros_semantico
