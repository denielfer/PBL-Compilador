import util
CoMF_CODE = 10
encode = "utf-8-sig"
import sys
console_print_stdout = sys.stdout

def analizar_lexico_files(paths:list[str]):
    from analizador_lexico import get_tokens, comentario_bloco_excption, CODIGOS
    sys.stdout = open('log_execução_lexico.txt', "w", encoding=encode)
    arquivos_lidos = []
    for path in paths:
        with open(path, 'r', encoding = encode) as file:
            new_file = path.replace('.txt', '-saida_lexico.txt')
            arquivos_lidos.append(new_file)
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
                                    out_file.write(f'{n} <{CODIGOS[token[0]]}, {token[1]}>\n')
                    # except analizador_lexico_recurcivo.comentario_linha_excption: # se recebeu essa excption so seguirmos, ela é usada para parar a recurção
                    #     pass  
                    # except analizador_lexico_recurcivo.comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                    except comentario_bloco_excption as e: # se recebemos excption para buscar comentario de bloco
                        FBC = True
                        TEXT_FBC = str(e)
                        LINE_FBC = n
                if erros:
                    out_file.write("\nErros:\n")
                    for erro in erros:
                        out_file.write(erro)
                else:
                    out_file.write("A análise léxica foi realizada com sucesso e não identificou nenhum erro de má formação.")

                if FBC: # terminou o arquivo e ta com comentario de bloco sem termina
                    out_file.write(f'{LINE_FBC + 1} <{CODIGOS[CoMF_CODE]}, {TEXT_FBC}>\n')
    return arquivos_lidos

def analizador_sintatico_files(paths:list):
    import re
    from analizador_sintatico import analize,erro_sintaico,file_end
    sys.stdout = open('log_execução_sintatico.txt', "w", encoding=encode)
    # sys.stdout = console_print_stdout
    arquivos_lidos = []
    regex_line = r'(\d)+\s\<(.+)\,\ (.+)\>'

    for path in paths:
        with open(path, 'r', encoding = encode) as file:
            new_file = path.replace('_lexico.txt', '.txt')
            arquivos_lidos.append(new_file)
            list_tokens = []
            for line in file.readlines():
                if line[0].isdigit():
                    result = re.match(regex_line,line)
                    list_tokens.append({'line':result.group(1),'type':result.group(2),'token':result.group(3)})
                    # print(result.groups())
                else:
                    break
            with open(new_file, 'w', encoding = encode) as out_file:
                try:
                    analize(list_tokens)
                    out_file.write('tudo certo por aqui')
                except erro_sintaico or file_end as e:
                    out_file.write('Erro sintatico:\n')
                    out_file.write(str(e))
                    print(e)

if __name__ == '__main__':
    
    paths = util.load_files()
    if not paths:
        print('Nenhum arquivo encontrado')
        exit()
    arquivos_lexico = analizar_lexico_files(paths)
    analizador_sintatico_files(arquivos_lexico)
