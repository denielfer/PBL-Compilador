import util
import analizador_lexico_recurcivo
paths = util.load_files()
if not paths:
    print('Nenhum arquivo encontrado')
    exit()
CoMF_CODE = 10
for path in paths:
    with open(path,'r') as file:
        with open(path.replace("input",'output',1)
                  .replace('.txt','-saida.txt'),'w') as out_file:
            FBC = False #flag_bloco_de_comentario = False
            TEXT_FBC = ''
            LINE_FBC = -1
            erros = []
            for n,line in enumerate(file.readlines()):
                line = line[:-1] if line[-1] == '-1' else line
                if not FBC:
                    try:
                        for token in analizador_lexico_recurcivo.get_token(line,
                                                            analizador_lexico_recurcivo.prioridade,
                                                            analizador_lexico_recurcivo.comportamentos):
                                if token[0]>8:
                                    erros.append(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]},{token[1]}>\n')
                                else:
                                    out_file.write(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]},{token[1]}>\n')
                    except analizador_lexico_recurcivo.comentario_linha_excption:
                        pass  
                    except analizador_lexico_recurcivo.comentario_bloco_excption as e:
                        FBC = True
                        TEXT_FBC = str(e)
                        LINE_FBC = n
                else:
                    if '*/' in line:
                        FBC = False
                        line = line.split('*/',1)[1]
                        try: # sim é o mesmo codigo de cima, preguiça de tranforma numa função e fica passando e vontando com variavel
                            for token in analizador_lexico_recurcivo.get_token(line,
                                                                analizador_lexico_recurcivo.prioridade,
                                                                analizador_lexico_recurcivo.comportamentos):
                                if token[0]>8:
                                    erros.append(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]},{token[1]}>\n')
                                else:
                                    out_file.write(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]},{token[1]}>\n')
                        except analizador_lexico_recurcivo.comentario_linha_excption:
                            pass  
                        except analizador_lexico_recurcivo.comentario_bloco_excption as e:
                            FBC = True
                            TEXT_FBC = str(e)
                    else:
                        TEXT_FBC +=line
            for erro in erros:
                out_file.write(erro)
            if FBC: # terminou o arquivo e ta com comentario de bloco sem termina
                out_file.write(f'{LINE_FBC} <{analizador_lexico_recurcivo.codigos[CoMF_CODE]},{TEXT_FBC}>\n')