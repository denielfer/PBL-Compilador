TYPE = ['int', 'real', 'boolean', 'string']
TYPES = TYPE +['void'] # menos IDE

ART = ['+', '-', '*', '/']

ART_DOUBLE = ['++', '--']

REL =  ['<', '<=', '>', '>=', '!=', '==']

LOG = ['&&', '||']

BOOL = ['true', 'false']

get_functions = {
    'const':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['const'],'next':[('const',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('const',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('const',2),('const',3)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('const',4)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('const',5)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value": BOOL,'next':[('const',6)]},
                    {'is_terminal':True,"key":'type',"value": ['NRO','CAC'],'next':[('const',6)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value": [','],'next':[('const',3)]},
                    {'is_terminal':True,"key":'token',"value": [''],'next':[(";",0)]},
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
                        {'is_terminal':True,"key":'token',"value":TYPE,'next':[('variables',2),('variables',3)]},
                        {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('variables',4),('dimention_acess',0)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                    {"test":[
                        {'is_terminal':True,"key":'token',"value": [','],'next':[('variables',3)]},
                    {'is_terminal':True,"key":'token',"value": [''],'next':[(";",0)]},
                    ],'erro':{'tipo_recuperação':'next'}},
                ],
    'class': [
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['class'],'next':[('class',1)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ 
                # ('end_block',0) é colocado aqui pois da forma como é feita ao colocar no 4 daria problema com empacota construtor, precisando de branch para main e classe normal assim colocando aqui reduz codigo
                    {'is_terminal':True,"key":'token',"value":['main'],'next':[('end_block',0),('class',5)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('class',0),('end_block',0),('constructor',0),('class',2)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['extends'],'next':[("class",3)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[("class",4)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                  {'is_terminal':True,"key":'type',"value":['IDE'],'next':[("class",4)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('methods',0),('object',0),("variables",0)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('methods',2),('object',0),("variables",0)]}
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
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object',2),('object',3)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object',4),('dimention_acess',0)]},
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
                {"test":[ # para main pois precisamos forma função main como primeira e ela é diferente
                   {'is_terminal':True,"key":'token',"value":['methods'],'next':[('methods',3)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('func_dec',0),('func_main',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
               ],
    'func_main':[
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPES,'next':[('func_main',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['main'],'next':[('func_main',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('func_dec',3),("close_parentesis",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'func_dec':[
                {'test':[
                    {'is_terminal':True,"key":'token',"value":TYPES,'next':[('func_dec',1)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('func_dec',1)]},
                    {'is_terminal':True,"key":'type',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('func_dec',0),('func_dec',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('func_dec',3),("close_parentesis",0),('dec_parameter',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {'test':[
                    {'is_terminal':True,"key":'token',"value":['{'],'next':[('end_block',0),('return',0),("command",0),('object',0),('variables',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'return':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['return'],'next':[('return',1)]}
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':False,'terminais':[('value',0)],'next':[(";",0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[(";",0)]},
                ],'erro':{'tipo_recuperação':'next'}
                },
            ],
    'end_block':[ # ("end_block",0),
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['}'],'next':[]}
                ],'erro':{'tipo_recuperação':'next'}}
                ],
    'dec_parameter':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('dec_parameter',1)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('dec_parameter',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'mult_dec_parameter':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":[','],'next':[('mult_dec_parameter',1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":TYPE,'next':[('mult_dec_parameter',2)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',2)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('mult_dec_parameter',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
    ],
    'command':[
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['print'],'next':[('command',0),(";",0),('print',0)]},
                    {'is_terminal':True,"key":'token',"value":['read'],'next':[('command',0),(";",0),('read',0)]},
                    {'is_terminal':True,"key":'token',"value":['if'],'next':[('command',0),('if',0)]},
                    {'is_terminal':True,"key":'token',"value":['for'],'next':[('command',0),('for',0)]},
                    {'is_terminal':True,"key":'type' ,"value":['IDE'],'next':[('command',0),('assigment_or_method_acess_or_duble',0)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    'assigment_or_method_acess_or_duble':[
                {"test":[
                    {'is_terminal':False,'terminais':[('dimention_acess',0)],'next':[("assigment_or_method_acess_or_duble",1),('object_access',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['->'],'next':[(';',0),('method_access',1)]},
                    {'is_terminal':True,"key":'token',"value":['='],'next':[(';',0),('value',0)]},
                    {'is_terminal':True,"key":'token',"value":ART_DOUBLE,'next':[(';',0)]},
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
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('var_assinement',1),('object_access',0),("dimention_acess",0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ 
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('value',0)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[ # <ASSIGNMENT>
                    {'is_terminal':True,"key":'token',"value":['='],'next':[('value',0)]},
                    {'is_terminal':True,"key":'token',"value":ART_DOUBLE,'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
            ],
    'value':[
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['NRO'],'next':[("arit_expression",0)]},
                    {'is_terminal':True,"key":'type',"value":['CAC'],'next':[]},
                    {'is_terminal':True,"key":'token',"value":['['],'next':[("vetor_assinement",0)]},
                    {'is_terminal':True,"key":'token',"value":['!'],'next':[('logical_expression',1),('logical_expression',0)]},
                    {'is_terminal':True,"key":'token',"value":['('],'next':[('aritimetic_or_logical_parentesis_expression',0)]},
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('aritimetic_or_logical_expression',0),('object_access',0),("dimention_acess",0)]},
                    {'is_terminal':True,"key":'token' ,"value":BOOL,'next':[]},
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
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object_access',0),("dimention_acess",0)]},
                ],'erro':{'tipo_recuperação':'next'}}
    ],
    "print":[ 
                {"test":[
                    {'is_terminal':True,"key":'token',"value":['('],'next':[("close_parentesis",0),('print',1)]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE'],'next':[('object_access',0),("dimention_acess",0)]},
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
                    {'is_terminal':True,"key":'token',"value":['['],'next':[("dimention_acess",1)]},
                    {'is_terminal':True,"key":'token',"value":[''],'next':[]},
                ],'erro':{'tipo_recuperação':'next'}},
                {"test":[
                    {'is_terminal':True,"key":'type',"value":['IDE','NRO'],'next':[("dimention_acess",2)]},
                ],'erro':{'tipo_recuperação':'next'}},
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


def __get_list_actions__(stage:str,pos_stage:int):
    list_actions_return = []
    for ac in get_functions[stage][pos_stage]['test']:
        if ac['is_terminal']:
            # print(f'\t\tis_terminal ->{ac}')
            list_actions_return.append(ac)
        else:
            for nao_terminal in ac['terminais']: 
                # nao lida com indeterminação, se tiver 2 caminhos pra ide vai ir no que aparecer primeiro na lista
                # se tiver '' nas produções do action ele vai ser chamado assim q aparecer na lista la embaixo o que gera problema, 
                #    entao nao chama isso para nao-terminal que tenha '' nas produções
                for action_new in __get_list_actions__(*nao_terminal):
                    new_dic = action_new.copy()
                    new_dic['next'] = ac['next'] + action_new['next']
                    list_actions_return.append(new_dic)
                    # print(f'\t\tis not terminal -> {new_dic}, -> adicionado {ac["next"]}')
    return list_actions_return

def analize(get_token:list):
    stack = [('END',0),('class',0),('variables',0),("const",0)]
    stage = None
    for token in get_token:
        if token['token'] in ['this','constructor']:
            token['type'] = 'IDE'
        flag = True # se tiver produção vazia continuamos a analize com o mesmo token
        while flag: # ta aqui pra suporta produção vazia
            stage,pos_stage = stack.pop(-1) # por ser pop em '-1' le a pilha da direita pra esquerda
            print('\t',stage,pos_stage,'token : ',token,' |',' stack :',stack)
            flag = False
            if stage == 'END':
                yield f"Na linha {token['line']}, era esperado 'EOF' porém foi obtido {token['token']}"
                stack.append(('END',0))
                continue
            list_actions = __get_list_actions__(stage,pos_stage)
            esperado = []
            for action in list_actions: # para cada token na lista de tokens esperados
                print(f'\t\tbuscando {action}')
                if token[action['key']] in action["value"]: # verifica se o token é o esperado
                    for item in action["next"]:
                        stack.append(item)
                    break
                # pode dar merda se vazil nao for o primeiro token
                elif "" in action["value"]: # se for token vazio continuamos em busca pelo proximo elemento q vem
                    for item in action["next"]:
                        stack.append(item)
                    flag = True
                    break
                else: # se nao é token esperado e o nao tem token vazio esperado adicionamos a lsita de esperados
                    esperado += action["value"] 
            else: # se nao acho ação para token é pq é token nao esperado
                esperado = str(esperado).replace("'IDE'","IDE").replace("'NRO'","NRO").replace("'CAC'","CAC")
                if get_functions[stage][pos_stage]['erro']['tipo_recuperação'] == 'next':
                    print(f'\t\t\tmodo thiago segue pra frente -> Na linha {token["line"]}, era esperado {esperado} porém foi obtido \'{token["token"]}\'')
                    for item in list_actions[-1]["next"]: # adiciona a pilha a ultima possibilidade do token
                        stack.append(item)
                    pass
                yield f"Na linha {token['line']}, era esperado {esperado} porém foi obtido \'{token['token']}\' "
    else:# quando os tokens acabarem
        for item in stack[::-1]: # para cada item na stack
            stage, pos_stage = item
            if stage != 'END': # se nao for o fim gera o erro
                list_actions = get_functions[stage][pos_stage]['test']
                esperado = []
                for action in list_actions:
                    esperado += action["value"] 
                esperado = str(esperado).replace("'IDE'","IDE").replace("'NRO'","NRO").replace("'CAC'","CAC")
                yield f"Na linha {token['line']+1}, era esperado {esperado} porém foi obtido 'EOF'"
        
