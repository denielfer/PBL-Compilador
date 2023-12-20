class Semantico():
    def __init__(self):
        self.data = {}
        self.stack = []

    #{'line':n, 'type':CODIGOS[token[0]], 'token':token[1]}
    def insert(self,token:dict,type:str,scopo:list[str]):
        self.data[''.join(scopo)+token['token']] = { 'type':type }
    
    def __getitem__(self,key):
        return self.data.get(key)

    def get(self,token:dict,scopo:list[str],default=None):
        return self.data.get(''.join(scopo)+token['token'],default)
        
    def append(self,data):
        self.stack.append(data)
    
    def pop(self,n:int=-1):
        return self.stack.pop(n)