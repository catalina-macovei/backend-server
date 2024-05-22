import subprocess, sys, os

# comenzile de executie in functie de limbaj
commands = {
    "python": {
        "filename": "python_code.py",
        "command": ["python", "python_code.py"]
    },
    "cpp": {
        "filename": "cpp_code.cpp",
        "command": "./cpp_code"
    }
}

# cod sursa:
python_code = """
print('Hello, world!')
x = 5
y = 10
print(f'The sum of x and y is {x + y}')
"""

cpp_code = """
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    int x = 5;
    int y = 10;
    std::cout << "The sum of x and y is " << x + y << std::endl;
    return 0;
}
"""


# lista de teste
# to do: o fct care primeste ca parametru fisierul de teste si returneaza lista
test_cases = [
    {
        "input": [],
        "output": "Hello, world!\nThe sum of x and y is 15\n"
    },
    {
        "input": [],
        "output": "Hello, world!\nThe sum of x and y is 15\n"
    }
]

def write_code_to_file(code, filename): # mai tarziu rulez fisierul in linie de comanda
    with open(filename, 'w') as file:
        file.write(code)

def compile_cpp_code(filename):
    try:
        compilation_output = subprocess.check_output(
            ["g++", "-std=c++14", filename, "-o", "cpp_code"],
            stderr=subprocess.STDOUT,
            text=True
        )
        print("C++ code compiled successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling C++ code: {e.output}")
        exit(1)

def execute_program(command, inputs):
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        actual_output, _ = process.communicate(input="\n".join(inputs) + "\n")
        return actual_output
    except subprocess.CalledProcessError as e:
        return e.output

# verific dc este python instalat
def find_python_env():
    try:
        subprocess.run(["python", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.run(["python3", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # update comanda
            commands["python"]["command"] = ["python3", "python_code.py"]
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Python interpreter not found...")
            exit(1)

# rulez testele
def run_test_cases(test_cases, lang, commands):
    test_results = []
    for i, test_case in enumerate(test_cases):
        output = execute_program(commands[lang]["command"], test_case["input"])
        print(f"Test case #{i + 1}: {output}")
        # compar output de la expected si actual
        if output == test_case["output"]:
            test_results.append((i + 1, True, output))
        else:
            test_results.append((i + 1, False, output, test_case["output"]))
    return test_results

def write_test_results(test_results, output_file_name):
    with open(output_file_name, "w") as output_file:
        for result in test_results:
            if result[1]:
                print(f"Test {result[0]}: PASSED")
                output_file.write(f"Test {result[0]}: PASSED\n")
            else:
                print(f"Test {result[0]}: FAILED")
                print(f"Expected: {result[3]}")
                print(f"Actual: {result[2]}")
                output_file.write(f"Test {result[0]}: FAILED\n")
                output_file.write(f"Expected: {result[3]}\n")
                output_file.write(f"Actual: {result[2]}\n")

# Clean up
def cleanup(lang):
    if lang == "python":
        if os.path.exists(commands["python"]["filename"]):
            os.remove(commands["python"]["filename"])
    elif lang == "cpp":
        if os.path.exists(commands["cpp"]["filename"]):
            os.remove(commands["cpp"]["filename"])
        if os.path.exists("cpp_code"):
            os.remove("cpp_code")

# logica rulare fisiere
def execute_test_cases(code, test_cases, lang, commands):
    if lang == "python":
        find_python_env()
        write_code_to_file(code, commands["python"]["filename"])
    elif lang == "cpp":
        write_code_to_file(code, commands["cpp"]["filename"])
        compile_cpp_code(commands["cpp"]["filename"])  # codul cpp trebuie compilat

    test_results = run_test_cases(test_cases, lang, commands)
    write_test_results(test_results, "../test_results.txt")
    cleanup(lang)

    return test_results

