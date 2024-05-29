from fastapi import FastAPI, HTTPException
from typing import Any, Dict
from pydantic import BaseModel
import traceback
from solutions.utilities import *
class Question(BaseModel): # obiectul Question mosteneste Base model (p/u serializarea datelor/validarea)
    id: int
    solution: str   # stocarea corpului functiei (codului de compilat de tip str)
    test_cases_filename: str # denumirea fisierului cu test cases

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

        test_cases = prepare_test_cases()
        result = execute_test_cases(function_code, test_cases, "cpp", commands)
        print("received response here", result)
        res = 200
        return {"result": res}

    except Exception as e:
        print(f"Exception occurred: {e}")
        # exceptia generata in timpul executiei
        raise HTTPException(status_code=404, detail="execution failed")
