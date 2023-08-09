import util
paths = util.load_files()
if not paths:
    print('Nenhum arquivo encontrado')
    exit()
for path in paths:
    with open(path,'r') as file:
        with open(path.replace("input",'output',1)
                  .replace('.txt','-saida.txt'),'w') as out_file:
            for char in "".join(file.readlines()):
                out_file.write(char+'\n')
