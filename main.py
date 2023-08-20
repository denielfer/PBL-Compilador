import util
import analizador_lexico_recurcivo

CoMF_CODE = 10

def analizar_lexico_files(paths:list[str]):
    for path in paths:
        with open(path, 'r') as file:
            with open(path.replace('.txt', '-saida.txt'), 'w') as out_file:
                FBC = False #flag_bloco_de_comentario = False
                TEXT_FBC = '' # texto comentario de bloco
                LINE_FBC = -1 # linha que acontece
                erros = []
                for n, line in enumerate(file.readlines()):
                    n+=1 # normalizar ( questao index vs posição natural )
                    line = line[:-1] if line[-1] == '\n' else line # remove o \n do final da linha se existir que seria a quebra de linha, nao gera erro caso o arquivo termine em \n como visto no 10.txt
                    if FBC: # se estamos em erro de bloco
                        if '*/' in line:
                            FBC = False
                            line = line.split('*/', 1)[1]
                        else: # se nao fecha nessa linha pulamos a analize dela
                            TEXT_FBC += line
                            continue
                    try:
                        for token in analizador_lexico_recurcivo.processar_string(line,
                                                            analizador_lexico_recurcivo.prioridade,):
                                if token[0] > 8: # se token for de erro vai pra lista
                                    erros.append(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]}, {token[1]}>\n')
                                else:# se nao escrevemos
                                    out_file.write(f'{n} <{analizador_lexico_recurcivo.codigos[token[0]]}, {token[1]}>\n')
                    except analizador_lexico_recurcivo.comentario_linha_excption: # se recebeu essa excption so seguirmos, ela é usada para parar a recurção
                        pass  
                    except analizador_lexico_recurcivo.comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                        FBC = True
                        TEXT_FBC = str(e)
                        LINE_FBC = n
                        

                for erro in erros:
                    out_file.write(erro)

                if FBC: # terminou o arquivo e ta com comentario de bloco sem termina
                    out_file.write(f'{LINE_FBC + 1} <{analizador_lexico_recurcivo.codigos[CoMF_CODE]}, {TEXT_FBC}>\n')


if __name__ == '__main__':
    
    paths = util.load_files()
    if not paths:
        print('Nenhum arquivo encontrado')
        exit()
    analizar_lexico_files(paths)