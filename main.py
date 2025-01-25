from fastapi import FastAPI, HTTPException, Header
from typing import Any, Dict, Optional
from pydantic import BaseModel
import json, traceback
from solutions.utilities import *
from dotenv import load_dotenv
from middleware import APIKeyMiddleware
from rate_limit_middleware import RateLimitMiddleware

class Question(BaseModel): # obiectul Question mosteneste Base model (p/u serializarea datelor/validarea)
    id: int
    solution: str   # stocarea corpului functiei (codului de compilat de tip str)
    lang: str
    test_cases: str  # stringul cu test cases petru exercitiu

load_dotenv()

app = FastAPI()
# Add the middleware to the FastAPI app
app.add_middleware(APIKeyMiddleware)
app.add_middleware(RateLimitMiddleware)
@app.post("/execute")
async def execute_code(question: Question,
    x_api_key: Optional[str] = Header(None) ):
    print(question, f"x-api-key: {x_api_key}")
    print(f"Executing solution for {question.id}")
    try:
        function_code = question.solution
        print(function_code)

        if not function_code:
            raise ValueError("No function code provided")

        test_cases_obj = prepare_test_cases(question.test_cases)
        result = execute_test_cases(function_code, test_cases_obj, question.lang, commands)
        print("Received response", result)

        if not result:
            raise ValueError("Execution did not return any result")

        # Returnare raspuns in format json
        result_json = json.dumps(result)
        return {"result": result_json}

    except ValueError as ve:
        print(f"ValueError occurred: {ve} !")
        raise HTTPException(status_code=400, detail=str(ve))

    except json.JSONDecodeError as je:
        print(f"JSONDecodeError occurred: {je}")
        raise HTTPException(status_code=422, detail="Invalid JSON format in the response!")

    except Exception as e:
        print(f"Exception occurred: {e}")
        raise HTTPException(status_code=404, detail="Execution code failed!")
