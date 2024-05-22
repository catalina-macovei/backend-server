from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from pydantic import BaseModel
from solutions.router import route

import traceback

class Question(BaseModel): # obiectul Question mosteneste Base model (p/u serializarea datelor/validarea)
    id: int
    solution: str   # stocarea corpului functiei (codului de compilat de tip str)

app = FastAPI()

@app.post("/execute")
async def execute_code(question: Question):
    print(f"executing solution for {question.id}")
    # 200 - success
    # 400 - bad request
    # 422 - validation err
    try:
        function_code = question.solution
        print(function_code)

        # executarea codului python
        exec_globals = {}  # creare context nou de executie

        # in loc de asta, exec(fisier_executabil, params) -> gcc ./exe
        exec(function_code, globals(), exec_globals) # codul executat are acces la contextul global al modului exec
        result = route(question.id, exec_globals) # redirectioneaza la functia de test corespunzatoare
        print("received response here", result)

        return {"result": result}

    except Exception as e:
        print(f"Exception occurred: {e}")
        # exceptia generata in timpul executiei
        raise HTTPException(status_code=404, detail="execution failed")

