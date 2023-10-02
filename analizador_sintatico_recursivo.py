def __const__(token_list,pos):
    if token_list[pos] == 'const':
        pos+=1
        if token_list[pos] == '{':
            pos+=1
            dec_const(token_list,pos)
            if token_list[pos] == '}':
                pos+=1
            else:
                pass
        else:
            pass
    else:
        pass
    return pos