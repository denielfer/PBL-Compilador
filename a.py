def load_files(base_dir:str = 'files') -> list[str]:
    '''
        Pega caminho relativo de todos arquivos com terminação '.txt' de apartir 
            de um diretorio raiz
    '''
    #coloque aqui o caminho da pasta das imagens
    from os import walk, path
    returned = {}
    for (dirpath, dirnames, filenames) in walk(base_dir):
        for filename in filenames: 
            returned[filename] = path.join(dirpath, filename)
    return returned

output = load_files('files')
old_output = load_files('_files')

with open('compare.txt','w') as f:
    for a in output:
        f.write(f'Comparando: {a}\n')
        b = old_output[a]
        a = output[a]
        c = 0
        with open(a,'r') as f1:
            with open(b,'r') as f2:
                l1 = f1.readlines()
                l2 = f2.readlines()
                for l1,l2 in zip(l1,l2):
                    if l1 != l2:
                        f.write(f' Linhas diferentes: {c+1}\n')
                        f.write(f'\t{l1}')
                        f.write(f'\t{l2}')
                    c+=1
    f.write(f'______________________________________\n\n')