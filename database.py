from find_toppers import find_toppers
import json 

def database(dept, year, semester, batch, subject):
    try:
        with open("db.json", 'r') as f:
            db = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {} 

    code = dept+year+semester+batch+subject
    if code in db:
        if type(db[code]) == str:
             result = find_toppers(dept, year, semester, batch, subject)
        result = db[code]
    else:
        result = find_toppers(dept, year, semester, batch, subject)
        if not type(result) == str:
          db[code] = result

    
    with open("db.json", 'w') as f:
        json.dump(db, f, indent=4)

    return result
