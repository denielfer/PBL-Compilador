import util
paths = util.load_files()
if len(paths)==0:
    print('Nenhum arquivo encontrado')
    exit()
print(1)
for path in paths:
    with open(path,'r') as file:
        with open(path.replace("input",'output',1)
                  .replace('.txt','-saida.txt'),'w') as out_file:
            for char in "".join(file.readlines()):
                out_file.write(char+'\n')
