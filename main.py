import util
from Analizador_lexico import CoMF_CODE # codigo de cadeia mal formada
encode = "utf-8-sig"
import sys
console_print_stdout = sys.stdout

def analizar_lexico_files(path:str,replace='.txt',replace_to='-saida.txt'):
    from Analizador_lexico import get_tokens, comentario_bloco_excption, CODIGOS
    tokens_corretos=[]
    with open(path, 'r', encoding = encode) as file:
        new_file = path.replace(replace, replace_to)
        with open(new_file, 'w', encoding = encode) as out_file:
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
                                tokens_corretos.append({'line':n, 'type':CODIGOS[token[0]], 'token':token[1]})
                                out_file.write(f'{n} <{CODIGOS[token[0]]}, {token[1]}>\n')
                # except analizador_lexico_recurcivo.comentario_linha_excption: # se recebeu essa excption so seguirmos, ela é usada para parar a recurção
                #     pass  
                # except analizador_lexico_recurcivo.comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                except comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                    FBC = True
                    TEXT_FBC = str(e)
                    LINE_FBC = n
            if erros:
                out_file.write("\n\nErros:\n")
                for erro in erros:
                    out_file.write(erro)
            else:
                out_file.write("\n\nA análise léxica foi realizada com sucesso e não identificou nenhum erro de má formação.")

            if FBC: # terminou o arquivo e ta com comentario de bloco sem termina
                out_file.write(f'{LINE_FBC + 1} <{CODIGOS[CoMF_CODE]}, {TEXT_FBC}>\n')
    return tokens_corretos,new_file

def analizador_sintatico_files(list_tokens:list[dict], path:str,log_sem):
    print(path)
    print('\n\n',path,file=log_sem)
    from Analizador_sintatico import analize
    erros = []
    analizer = analize(list_tokens,log_sem)
    semantico = None
    try:
        while True:
            erro = next(analizer)
            erros.append(erro)
    except StopIteration as e:
        semantico = e
    with open(path, 'a', encoding = encode) as out_file:
        if erros != []:
            out_file.write('\n\nErros Sintaticos identificados:\n')
            for erro in erros:
                out_file.write(f'{erro}\n')
        else:
            out_file.write(f'\n\nSem erros Sintaticos')
        # sys.stdout = log_sem
        print("___________________", file= log_sem)
        print(semantico, file= log_sem)
        if semantico is None or semantico.__str__() == '[]':
            out_file.write(f'\n\nSem erros Semanticos')
        else:
            out_file.write('\n\nErros Semanticos identificados:\n')
            for s in str(semantico)[1:-1].replace('"',"'").split("', "):
                s= s.replace("'","")
                out_file.write(f'{s}\n')



if __name__ == '__main__':
    
    paths = util.load_files()
    if not paths:
        print('Nenhum arquivo encontrado')
        exit()
    log_lex =  open('logs/log_execução_lexico.txt', "w", encoding=encode)
    log_sint =  open('logs/log_execução_sintatico.txt', "w", encoding=encode)
    log_sem =  open('logs/log_execução_semantico.txt', "w", encoding=encode)
    for path in paths:
        # try:
            sys.stdout = log_lex
            tokens_corretos, new_file = analizar_lexico_files(path)
            sys.stdout = log_sint
            # sys.stdout = console_print_stdout
            # analizador_sintatico_files(tokens_corretos, new_file,console_print_stdout)
            analizador_sintatico_files(tokens_corretos, new_file,log_sem)
        # except Exception as e:
        #     import traceback
        #     sys.stdout = log_sem
        #     print(f'Erro irecuperavel no arquivo {path}', ':\n')
        #     print(traceback.format_exc())
        #     print('\n'*2)
