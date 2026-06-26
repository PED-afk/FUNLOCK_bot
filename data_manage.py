import json

def save_json(path:str,data:dict):
    with open(path,"w", encoding="utf-8") as f:
        return json.dump(data,f,indent=4,ensure_ascii=False)
    
def load_json(filePath:str):
    with open(filePath,"r", encoding="utf-8") as f:
        return json.load(f)

def load_txt(filePath:str):
    contents=[]
    with open(filePath,"r") as f:
        line=f.readline().strip()
        while line:
            contents.append(line)
            line=f.readline().strip()
    return contents

