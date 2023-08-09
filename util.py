def load_files(base_dir:str = 'files\\input') -> list[str]:
    '''
        Pega caminho relativo de todos arquivos com terminação '.txt' de apartir 
            de um diretorio raiz
    '''
    #coloque aqui o caminho da pasta das imagens
    from os import walk,path
    returned = []
    for (dirpath, dirnames, filenames) in walk(base_dir):
        for filename in filenames: 
            if filename.endswith(".txt"):
                returned.append(path.join(dirpath, filename))
    return returned

if __name__ == '__main__':
    # import sys
    # print(load_files(sys.argv[0]))
    print(load_files())
