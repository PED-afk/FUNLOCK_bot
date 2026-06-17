import json

def save_json(path:str,data:dict):
    with open(path,"w") as f:
        return json.dump(data,f,indent=4,ensure_ascii=False)
    
def load_json(filePath:str):
    with open(filePath,"r") as f:
        return json.load(f)



