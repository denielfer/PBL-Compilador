import re

txt = 'sadasd.dasd'

print('PRE:')
print(re.findall(r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b', txt))
print('NRO:')
print(re.findall(r'\b\d+\.?\d*\b', txt))
print('IDE:')
print(re.findall(r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b', txt))
print('CAC:')
print(re.findall(r'\".*\"', txt))
print('ART:')
print(re.findall(r'\+\+|--|[+*/-]', txt))
print('REL:')
print(re.findall(r'!=|==|<=|>=|[=<>]', txt))
print('LOG:')
print(re.findall(r'!|&&|\|\|', txt))
print('DEL:')
print(re.findall(r';|,|\.|\(|\)|\[|\]|\{|\}|->', txt))

# RegEx possíveis (use with findall)

# r'\b(variables|const|class|methods|objects|main|return|if|else|then|for|read|print|void|int|real|boolean|string|true|false)\b' PRE
# r'\b\d+\.?\d*\b' NRO
# r'\b[a-zA-Z]{1}\w*[^(\.\s)]\b' IDE
# r'\+\+|--|[+*/-]' ART
# r'!=|==|<=|>=|[=<>]' REL
# r'!|&&|\|\|' LOG
# r';|,|\.|\(|\)|\[|\]|\{|\}|->' DEL
# r'\".*\"' CAC