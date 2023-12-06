import re

txt = ' 3.3.3 6.a35&.99; 2.2. 1.1.1.! 9.0.0 10'

print(re.findall(r'\b\d+\.[^\d|^\/*|^\/\/][\w\.]*', txt))
print(re.findall(r'\b\d+(\.\d+)?', txt))

# print('PRE:')
# print(re.findall(r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b', txt))
# print('NRO:')
# print(re.findall(r'\b\d+(\.\d*)?\b', txt))
# print('IDE:')
# print(re.findall(r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b', txt))
# print('CAC:')
# print(re.findall(r'\b\".*\"\b', txt))
# print('ART:')
# print(re.findall(r'\+\+|--|[+*/-]', txt))
# print('REL:')
# print(re.findall(r'!=|==|<=|>=|[=<>]', txt))
# print('LOG:')
# print(re.findall(r'!|&&|\|\|', txt))
# print('DEL:')
# print(re.findall(r';|,|\.|\(|\)|\[|\]|\{|\}|->', txt))

# AQUI
# [^(\+\+|+|--|[+*/-]|\|\||&&|!|!=|==|<=|>=|[=<>]|;|,|\(|\)|\[|\]|\{|\}|->)]

# RegEx possíveis (use with findall)

# r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b' PRE
# r'\b\d+\.?\d*\b' NRO
# r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b' IDE
# r'\+\+|--|[+*/-]' ART
# r'!=|==|<=|>=|[=<>]' REL
# r'!|&&|\|\|' LOG
# r';|,|\.|\(|\)|\[|\]|\{|\}|->' DEL
# r'\".*\"' CAC