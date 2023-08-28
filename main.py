import util
from analizador_lexico import get_tokens, comentario_bloco_excption, CODIGOS
CoMF_CODE = 10
import sys
file_path = 'log_ultima_execução.txt'
sys.stdout = open(file_path, "w")

def analizar_lexico_files(paths:list[str]):
        for path in paths:
            with open(path, 'r', encoding = "utf8") as file:
                with open(path.replace('.txt', '-saida.txt'), 'w', encoding = "utf8") as out_file:
                    FBC = False # flag_bloco_de_comentario = False
                    TEXT_FBC = '' # texto comentario de bloco
                    LINE_FBC = -1 # linha que acontece
                    erros = []
                    for n, line in enumerate(file.readlines()):
                        n += 1 # normalizar ( questao index vs posição natural )
                        line = line[:-1] if line[-1] == '\n' else line # remove o \n do final da linha se existir que seria a quebra de linha, nao gera erro caso o arquivo termine em \n como visto no 10.txt
                        if FBC: # se estamos em erro de bloco
                            if '*/' in line:
                                FBC = False
                                line = line.split('*/', 1)[1]
                                # print(line)
                            else: # se nao fecha nessa linha pulamos a analize dela
                                TEXT_FBC += line
                                continue
                        try:
                            # for token in analizador_lexico_recurcivo.processar_string(line,
                            #                                     analizador_lexico_recurcivo.prioridade,):
                            for token in get_tokens(line):
                                    print(token)
                                    if token[0] > 8: # se token for de erro vai pra lista
                                        erros.append(f'{n} <{CODIGOS[token[0]]}, {token[1]}>\n')
                                    else: # se nao escrevemos
                                        out_file.write(f'{n} <{CODIGOS[token[0]]}, {token[1]}>\n')
                        # except analizador_lexico_recurcivo.comentario_linha_excption: # se recebeu essa excption so seguirmos, ela é usada para parar a recurção
                        #     pass  
                        # except analizador_lexico_recurcivo.comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                        except comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                            FBC = True
                            TEXT_FBC = str(e)
                            LINE_FBC = n
                            
                    print()
                    if erros:
                        print("Erros:")
                        for erro in erros:
                            out_file.write(erro)
                    else:
                        out_file.write("A análise léxica foi realizada com sucesso e não identificou nenhum erro de má formação.")

                    if FBC: # terminou o arquivo e ta com comentario de bloco sem termina
                        out_file.write(f'{LINE_FBC + 1} <{CODIGOS[CoMF_CODE]}, {TEXT_FBC}>\n')


if __name__ == '__main__':
    
    paths = util.load_files()
    if not paths:
        print('Nenhum arquivo encontrado')
        exit()
    analizar_lexico_files(paths)