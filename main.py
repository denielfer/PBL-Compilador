import util
import analizador_lexico_recurcivo
paths = util.load_files()
if not paths:
    print('Nenhum arquivo encontrado')
    exit()
for path in paths:
    with open(path,'r') as file:
        with open(path.replace("input",'output',1)
                  .replace('.txt','-saida.txt'),'w') as out_file:
            for n,line in enumerate(file.readlines()):
                line = line[:-1] if line[-1] == '-1' else line
                try:
                    for token in analizador_lexico_recurcivo.get_token(line,
                                                        analizador_lexico_recurcivo.prioridade,
                                                        analizador_lexico_recurcivo.comportamentos):
                        out_file.write(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]},{token[1]}>\n')
                except analizador_lexico_recurcivo.comentario_linha_excption:
                    pass               
