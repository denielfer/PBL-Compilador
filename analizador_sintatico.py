
# Tipos
TYPE = ['int', 'real', 'boolean', 'string']

# Tipos com void
TYPES = TYPE +['void'] # menos IDE

# Aritméticos simples
ART = ['+', '-', '*', '/']

# Aritméticos incremento
ART_DOUBLE = ['++', '--']

# Relacionais
REL =  ['<', '<=', '>', '>=', '!=', '==']

# Lógicos
LOG = ['&&', '||']

# Booleanos
BOOL = ['true', 'false']

# Gramática do Problema 2 ajustada
get_functions = {
    'const':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['const'],'next':[('const',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('const',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('const',2),('const',3)],'s':{'do':['append_stack']}},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('const',4)],'s':{'do':['insert_const_or_var','set_const'],'erro':[('const',6)]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('const',5)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value": BOOL,'next':[('const',6)],'s':{'do':['atr_const']}},
                    {'is_terminal':True,"key":'type',"value": ['NRO','CAC'],'next':[('const',6)],'s':{'do':['atr_const']}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value": [','],'next':[('const',3)]},
                    {'is_terminal':True,"key":'token',"value": [''],'next':[(";",0)],'s':{'do':["pop_stack"]}},
                ],'erro':{'tipo_recuperação':'next'}},
            ],
    'variables':[
                    {"test":[
                        {'is_terminal':True,"key":'token',"value":['variables'],'next':[('variables',1)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('variables',2)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'token',"value":TYPE,'next':[('variables',2),('variables',3)],'s':{'do':['append_stack']}},
                        {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('variables',4),('dimention_acess',0)],'s':{'do':['insert_const_or_var'],'erro':[('variables',4)]}},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'token',"value": [','],'next':[('variables',3)],'s':{'do':["pop_stack"]}},
                        {'is_terminal':True,"key":'token',"value": [''],'next':[(";",0)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                ],
    'class': [
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['class'],'next':[('class',1)],'s':{'do':['clear_stack']}}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ 
                # ('end_block',0) é colocado aqui pois da forma como é feita ao colocar no 4 daria problema com empacotar construtor, precisando de branch para main e classe normal, assim, colocando aqui reduz codigo
                    {'is_terminal':True,"key":'token',"value":['main'],'next':[('end_block',0),('class',5)],'s':{'do':['dec_class'], 'erro':[('class',0)]}},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('class',0),('end_block',0),('constructor',0),('class',2)],'s':{'do':['dec_class'], 'erro':[('class',0)]}}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['extends'],'next':[("class",3)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[("class",4)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                  {'is_terminal':True,"key":'type',"value":['IDE'],'next':[("class",4)],'s':{'do':['extends_class']}}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('methods',0),('object',0),("variables",0)],'s':{'do':['append_stack_class']}}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('methods',2),('object',0),("variables",0)],'s':{'do':['append_stack_class']}}
                ],'erro':{'tipo_recuperação':'next'}},
              ],
    'object':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['objects'],'next':[('object',1)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('object',2)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object',2),('object',3)],'s':{'do':['verify_type_class'], 'erro':[(";",0)]}},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object',4),('dimention_acess',0)],'s':{'do':['insert_object'], 'erro':[('object',4)]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value": [','],'next':[('object',3)]},
                    {'is_terminal':True,"key":'token',"value": [''],'next':[(";",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
            ],
    'methods' :[ 
                {"test":[
                   {'is_terminal':True,"key":'token',"value":['methods'],'next':[('methods',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('func_dec',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # para main pois precisamos formar a função main como primeira e ela é diferente
                   {'is_terminal':True,"key":'token',"value":['methods'],'next':[('methods',3)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('func_dec',0),('func_main',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
               ],
    'func_main':[
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPES,'next':[('func_main',1)],'s':{'do':['append_stack']}},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['main'],'next':[('func_main',2)],'s':{'do':['creat_func'], 'erro':[('func_dec',0)]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('func_dec',3),("close_parentesis",0)],'s':{'do':['move_param']}},
                ],'erro':{'tipo_recuperação':'next'}}, # tem move_param pois apesar de nao ter parametro, o proximo ('func_dec',3) começa com scopo.pop()
    ],
    'func_dec':[
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPES,'next':[('func_dec',1)],'s':{'do':['append_stack']}},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('func_dec',1)],'s':{'do':['append_stack']}},
                    {'is_terminal':True,"key":'type',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('func_dec',0),('func_dec',2)],'s':{'do':['creat_func'], 'erro':[('func_dec',0)]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('func_dec',3),("close_parentesis",0),('dec_parameter',0)],'s':{'do':['move_param']}},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('return',0),("command",0),('object',0),('variables',0)],'s':{'do':['change_scopo_to_data']}},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'return':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['return'],'next':[('return',1)],'s':{'do':['return_func_data']}}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':False,'terminais':[('value',0)],'next':[(";",0)],'s':{'do':['validate_return']}},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[(";",0)],'s':{'do':['validate_return_void']}},
                ],'erro':{'tipo_recuperação':'next'}},
            ],
    'end_block':[ # ("end_block",0),
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['}'],'next':[]}
                ],'erro':{'tipo_recuperação':'next'}}
                ],
    'dec_parameter':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('dec_parameter',1)],"s":{'do':['dec_param_type']}},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('dec_parameter',1)],"s":{'do':['dec_param_IDE']},'erro':[('mult_dec_parameter',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',0)],'s':{'do':['dec_param']}},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'mult_dec_parameter':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[','],'next':[('mult_dec_parameter',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('mult_dec_parameter',2)],"s":{'do':['dec_param_type']}},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',2)],"s":{'do':['dec_param_IDE'],'erro':[('mult_dec_parameter',0)]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',0)],'s':{'do':['dec_param']}},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'command':[#########################################################################################################################
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['print'],'next':[('command',0),(";",0),('print',0)]},
                    {'is_terminal':True,"key":'token',"value":['read'],'next':[('command',0),(";",0),('read',0)]},
                    {'is_terminal':True,"key":'token',"value":['if'],'next':[('command',0),('if',0)]},
                    {'is_terminal':True,"key":'token',"value":['for'],'next':[('command',0),('for',0)]},
                    {'is_terminal':True,"key":'type' ,"value":['IDE'],'next':[('command',0),('assigment_or_method_acess_or_duble',0)],'s':{'do':['validade_IDE',"add_void_stack"]}},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    'assigment_or_method_acess_or_duble':[
                {"test":[
                    {'is_terminal':False,'terminais':[('dimention_acess',0)],'next':[("assigment_or_method_acess_or_duble",1),('object_access',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['->'],'next':[(';',0),('method_access',1)],'s':{'do':['validate_last_object']}},####################################################################################
                    {'is_terminal':True,"key":'token',"value":['='],'next':[(';',0),('value',0)],'s':{'do':['atribuição']}},
                    {'is_terminal':True,"key":'token',"value":ART_DOUBLE,'next':[(';',0)],'s':{'do':['duble_art']}},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'for':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[
                                                                                ("if",4), # '{' <command> '}'
                                                                                ("close_parentesis",0),
                                                                                ('var_assinement',2),
                                                                                ('object_access',1),
                                                                                (";",0),
                                                                                ('relational_expression_value',2),
                                                                                ('relational_expression_value',1),
                                                                                (";",0),
                                                                                ('var_assinement',0),
                                                                            ]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'var_assinement':[
        # <ASSIGMENT_WITHOUT_SEMICOLON> -> index [0,1]
                {"test":[ # <DEC_OBJECT_ATRIBUTE_ACCESS>
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('var_assinement',1),('object_access',0),("dimention_acess",0)],'s':{'do':['validade_IDE',"add_void_stack"]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ 
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('value',0)],'s':{'do':['atribuição']}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # <ASSIGNMENT>
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('value',0)],'s':{'do':['atribuição']}},
                    {'is_terminal':True,"key":'token',"value":ART_DOUBLE,'next':[],'s':{'do':['duble_art']}},
                ],'erro':{'tipo_recuperação':'next'}},
            ],
    'value':[
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['NRO'],'next':[("arit_expression",0)],'s':{'do':['stack_NRO']}}, ################################################################################
                    {'is_terminal':True,"key":'type',"value":['CAC'],'next':[],'s':{'do':['stack_CAC']}},
                    {'is_terminal':True,"key":'token',"value":['['],'next':[("vetor_assinement",0)]},
                    {'is_terminal':True,"key":'token',"value":['!'],'next':[('logical_expression',1),('logical_expression',0)]},
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('aritimetic_or_logical_parentesis_expression',0)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('aritimetic_or_logical_expression',0),('object_access',0),("dimention_acess",0)]},
                    {'is_terminal':True,"key":'token' ,"value":BOOL,'next':[],'s':{'do':['stack_BOOL']}},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'aritimetic_or_logical_parentesis_expression':[
                {"test":[
                    {'is_terminal':False,'terminais':[('arit_expression',1)],'next':[("arit_expression",0),("close_parentesis",0)]},
                    {'is_terminal':False,'terminais':[('logical_expression',0)],'next':[
                                                                                                ("logical_expression",1),
                                                                                                ("close_parentesis",0),
                                                                                                ("logical_expression",1)
                                                                                            ]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'aritimetic_or_logical_expression':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['->'],'next':[('logical_expression',1),('relational_expression_value',0),('method_access',1)]},
                    {'is_terminal':True,"key":'token',"value":ART_DOUBLE,'next':[]},
                    {'is_terminal':True,"key":'token',"value":ART,'next':[('arit_expression',1)]},
                    {'is_terminal':True,"key":'token',"value":REL,'next':[('logical_expression',1),('relational_expression_value',1)]},
                    {'is_terminal':True,"key":'token',"value":LOG,'next':[('logical_expression',1),('logical_expression',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'logical_expression':[ 
        # <LOGICAL_EXPRESSION> -> todos
                {"test":[ # logical_expression_begin
                    {'is_terminal':True,"key":'token',"value":['!'],'next':[('logical_expression',0)]},
                    {'is_terminal':True,"key":'token',"value":['('],'next':[("close_parentesis",0),('logical_expression',1),('logical_expression',0)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[("relational_expression_value",0),('method_access',0),('object_access',0),("dimention_acess",0)]},
                    {'is_terminal':True,"key":'token',"value":BOOL,'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[# logical_expression_end
                    {'is_terminal':True,"key":'token',"value":LOG,'next':[('logical_expression',1),('logical_expression',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'relational_expression_value':[
        # index [1,2,1] -> <RELATIONAL_EXPRESSION>
                {"test":[ # <LOG_REL_OPTIONAL>
                    {'is_terminal':True,"key":'token',"value":REL,'next':[('relational_expression_value',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # <RELATIONAL_EXPRESSION_VALUE>
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('method_access',0),('object_access',0),("dimention_acess",0)]},
                    {'is_terminal':True,"key":'type',"value":['NRO','CAC'],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ 
                    {'is_terminal':True,"key":'token',"value":REL,'next':[('relational_expression_value',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'method_access':[
                {"test":[ # <optional_method_access>
                    {'is_terminal':True,"key":'token',"value":['->'],'next':[('method_access',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('method_access',2)]},
                    {'is_terminal':True,"key":'token',"value":['constructor'],'next':[('method_access',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('close_parentesis',0),("parameters",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['->'],'next':[('method_access',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'parameters':[
                {"test":[ #<PARAMETERS>
                    {'is_terminal':False,"terminais":[("value",0)],'next':[('parameters',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # <MULT_PARAMETERS>
                    {'is_terminal':True,"key":'token',"value":[','],'next':[('parameters',1),('value',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'vetor_assinement':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['['],'next':[('vetor_assinement',1),('vetor_assinement',0)]},
                    {'is_terminal':True,"key":'type',"value":['IDE','CAC','NRO'],'next':[('vetor_assinement',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[','],'next':[('vetor_assinement',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[('vetor_assinement',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[']'],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'arit_expression':[
                {"test":[ # <END_EXPRESSION_OPTIONAL>
                    {'is_terminal':True,"key":'token',"value":ART,'next':[('arit_expression',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ #<SIMPLE_EXPRESSION>
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('arit_expression',0),('object_access',0),("dimention_acess",0)]},
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('arit_expression',0),('close_parentesis',0),('arit_expression',1)]},
                    {'is_terminal':True,"key":'type',"value":['NRO'],'next':[('arit_expression',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # <END_EXPRESSION>
                    {'is_terminal':True,"key":'token',"value":ART,'next':[('arit_expression',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'if':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('if',1),("close_parentesis",0),('logical_expression',1),('logical_expression',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['then'],'next':[('if',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('if',3),("end_block",0),('command',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['else'],'next':[('if',4)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[("end_block",0),('command',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'read':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[("close_parentesis",0),('read',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object_access',0),("dimention_acess",0)],"s":{'do':['validade_is_str']}},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    "print":[ 
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[("close_parentesis",0),('print',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object_access',0),("dimention_acess",0)],'s':{'do':["validade_IDE","add_void_stack"]}},
                    {'is_terminal':True,"key":'type',"value":['CAC','NRO'],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    "close_parentesis":[ # ("close_parentesis",0),
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[')'],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    'dimention_acess':[ 
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['['],'next':[("dimention_acess",1)],'s':{'do':["validate_is_vector"]}},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[],'s':{'do':["pop_stack"]}},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE','NRO'],'next':[("dimention_acess",2)]},
                ],'erro':{'tipo_recuperação':'next'},'s':{'do':["validate_dimention_acess"]}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[']'],'next':[("dimention_acess",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['['],'next':[("dimention_acess",1)]},
                ],'erro':{'tipo_recuperação':'next'}},
               ],
    'object_access':[ 
        # <DEC_OBJECT_ATRIBUTE_ACCESS> -> começa do index 1
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['.'],'next':[("object_access",1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[("object_access",0),("dimention_acess",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
               ],
    ';':[ # (";",0),
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[';'],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
        ],
    'constructor':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['constructor'],'next':[("constructor",1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'is_terminal':True,"key":'token',"value":['('],'next':[('constructor',6),("close_parentesis",0),('constructor',2)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('constructor',3)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('constructor',3)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('constructor',4)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":[','],'next':[('constructor',5)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('constructor',3)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('constructor',3)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                        {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),("command",0),('object',0),('variables',0)]},
                    ],'erro':{'tipo_recuperação':'next'}},
            ],
}

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
                for action_new in _get_list_actions(*nao_terminal):
                    new_dic = action_new.copy()
                    new_dic['next'] = ac['next'] + action_new['next']
                    if 's' in ac:
                        if 's' not in new_dic:
                            new_dic['s'] = {'do':[]}
                        new_dic['s']['do'] += ac['s']['do']
                        if 'erro' in ac['s']:
                            new_dic['s']['erro'] += ac['s']['erro']
                    list_actions_return.append(new_dic)
                    # print(f'\t\tis not terminal -> {new_dic}, -> adicionado {ac["next"]}')
    return list_actions_return

# from _typeshed import SupportsWrite
# def analize(get_token:list,log_sem:SupportsWrite[str]):
def analize(get_token:list,log_sem):
    stack = [('END', 0), ('class', 0), ('variables', 0), ("const", 0)]
    stage = None
    tabela = {'global':{},'stack':[]}
    scopo = ["global"]
    erro_sem = None
    retorno_semantico = []
    for token in get_token:
        if token['token'] in ['this', 'constructor']:
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
                    if erro_sem:
                        if (stage,pos_stage) in erro_sem:
                            erro_sem = None
                    if erro_sem is None:
                        for ret in sem_analize(action,token,tabela,scopo,log_sem):
                            if ret is not None:
                                print(ret,file=log_sem)
                                retorno_semantico.append(ret)
                                if 'erro' in action['s']:
                                    erro_sem = action['s']['erro']
                    if 'programado' in tabela:
                        if tabela['programado'][-1]['when'] == (stage,pos_stage):
                            for func,args in tabela['programado'].pop()['do']:
                                ret = func(**args)
                                if ret is not None:
                                    print(ret,file=log_sem)
                                    retorno_semantico.append(ret)
                            if len(tabela['programado']) == 0:
                                del(tabela['programado'])

                    #     getattr(semant, get_functions[stage][pos_stage]['s']['do'])(**get_functions[stage][pos_stage]['s']['param'],token = token,scopo=scopo)
                    break
                # pode dar erro se vazio não for o primeiro token
                elif "" in action["value"]: # se for token vazio, continuamos em busca pelo próximo elemento
                    for item in action["next"]:
                        stack.append(item)
                    if erro_sem:
                        if (stage,pos_stage) in erro_sem:
                            erro_sem = None
                    if erro_sem is None:
                        for ret in sem_analize(action,token,tabela,scopo,log_sem):
                            if ret is not None:
                                print(ret,file=log_sem)
                                retorno_semantico.append(ret)
                                if 'erro' in action['s']:
                                    erro_sem = action['s']['erro']
                    flag = True
                    break
                else: # se não for o token esperado e não tiver token vazio esperado, adicionamos a lista de esperados
                    esperado += action["value"] 
            else: # se não achou ação para o token é porque é token não esperado
                esperado = str(esperado).replace("'IDE'","IDE").replace("'NRO'","NRO").replace("'CAC'","CAC")
                if get_functions[stage][pos_stage]['erro']['tipo_recuperação'] == 'next':
                    print(f'\t\t\tNa linha {token["line"]}, era esperado {esperado} porém foi obtido \'{token["token"]}\'')
                    for item in list_actions[-1]["next"]: # adiciona a pilha a última possibilidade do token
                        stack.append(item)
                    pass
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
    return retorno_semantico

def sem_analize(action,token,tabela,scopo,log_sem):
    if "s" in action:
        for controle in action['s']['do']:
            yield _sem(controle, token, tabela,scopo,log_sem)

import json

def log(func):

    def warp(controle:int, token:dict, tabela:dict,scopo:list[str],log_sem):
        print('-> '+controle,scopo,token,file = log_sem,sep=' | ')
        r = func(controle, token, tabela,scopo,log_sem)
        print('data:'+json.dumps(tabela['global'],indent=4),"stack:"+json.dumps(tabela['stack'],indent=4),sep='\n',file = log_sem)
        return r
    return warp

# to do : mudar para varias funçoes?
#          implementa no codigo a cima chamada
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
        # case 9:
        #     a = _get_scopo(tabela,scopo)
        #     if token["token"] not in a:
        #         # print(f'retorno {controle} - 1',file = log_sem)
        #         return f"Na linha {token['line']}, classe {token['token']} não foi declarado novamente"
        #     elif token["token"] in PRE:
        #         # print(f'retorno {controle} - 2',file = log_sem)
        #         return f"Na linha {token['line']}, {token['token']} foi declarado porém é palavra reservada"    
        #     a[token['token']] = {"type":tabela['stack'][-1],'is_instanciado':False,'is_vetor':False}
        #     tabela['stack'].append(token["token"])
        case 'verify_type_class':
            a = tabela['global']
            if token["token"] not in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, classe {token['token']} não foi encontrada"
            else:
                if a[token['token']]["type"] != 'class':
                    return f"Na linha {token['line']}, {token['token']} foi usado como classe porem é {a[token['token']]['type']}"
            tabela['stack'].append(token["token"])
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
            a[token['token']] = {"type":tabela['stack'][-2],"data":a[tabela['stack'][-2]]['data']}
        case 'pop_stack':
            # stack: ..., _
            tabela['stack'].pop()
            # stack: ...
        case 'clear_stack':
            # stack: ...
            tabela['stack'] = []
            # stack: 
        case 'creat_func':
            # stack: ..., tipo
            tipo = tabela['stack'].pop()
            # stack: ...
            a = _get_scopo(tabela,scopo)
            from analizador_lexico import PRE
            if token["token"] in a:
                # print(f'retorno {controle} - 1',file = log_sem)
                return f"Na linha {token['line']}, {token['token']} declarado novamente"
            elif token["token"] in PRE and token['token'] != "main":
                # print(f'retorno {controle} - 2',file = log_sem)
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
            a['data'] = a['param']
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
            # stack: ...,func
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
            a[token['token']] = {'type':tipo}
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
        # case 'end_func':
        #     if 'programado' not in tabela:
        #         tabela['programado'] = []
        #     tabela['programado'].append({'when':("end_block",0),'do':[
        #                                                  (duble_pop,
        #                                                     {
        #                                                         'scopo':scopo
        #                                                     }
        #                                                  )
        #                                                 ]
        #                             }
        #                            )
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
                return f"Na linha {token['line']}, variavel {token['token']} não foi encontrada"  
            if a[var]['type'] != 'string':
                return f"Na linha {token['line']}, tentativa de carregar string em {var} porém esta é {a[var]['type']}"
        case 'stack_NRO':
            if '.' in token['token']:
                tabela['stack'].append('real')
            else:
                tabela['stack'].append('int')
        case 'stack_CAC':
                tabela['stack'].append('string')
        case 'stack_BOOL':
                tabela['stack'].append('boolean')

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

def _get_in_scopo(var, tabela,scopo):
    a = tabela
    for s in scopo:
        a = a[s]
    if var not in a:
        a = tabela['global']
    return a

def _get_scopo(tabela,scopo):
    a = tabela
    for s in scopo:
        a = a[s]
    return a
