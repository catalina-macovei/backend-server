# solutions_router.py

def route(solution_id, exec_globals):
    if solution_id == 2:
        print(f"checking solution for question {solution_id}")
        return checkQuestionSum(exec_globals)
    if solution_id == "sort-three":
        print(f"checking solution for question {solution_id}")
        return checkQuestionSortThree(exec_globals)
    else:
        print(f"no path provided")
        return 0


'''
to do tests, in fct de testul failed -> raise exception:
"t1": {
            "name": 'Expect 15',
            "x": 5,
            "y": 10,
            "result": 15
        }
'''
def checkQuestionSum(exec_globals):
    function = exec_globals.get("add")
    params = {
        "x": 5,
        "y": 10
    }
    result = function(**params)
    return result

def checkQuestionSortThree(exec_globals):
    function = exec_globals.get("sort_three")
    params = {
        "x": 5,
        "y": 10,
        "z": 1
    }
    result = function(**params)

    return result

