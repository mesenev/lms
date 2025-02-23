import sys
import json
import subprocess
import time

def run_python_code(code, input_data):
    start_time = time.time()
    try:
        result = subprocess.run(
            ["python3", "-c", code], 
            input=input_data.encode(), 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        output = result.stdout.strip()
    except subprocess.TimeoutExpired:
        output = "TIMEOUT"
    
    return output, time.time() - start_time

def run_cpp_code(code, input_data):
    with open("solution.cpp", "w") as f:
        f.write(code)

    compile_proc = subprocess.run(["g++", "solution.cpp", "-o", "solution"], capture_output=True, text=True)
    if compile_proc.returncode != 0:
        return compile_proc.stderr.strip(), 0
    
    start_time = time.time()
    try:
        result = subprocess.run(
            ["./solution"], 
            input=input_data.encode(), 
            capture_output=True, 
            text=True, 
            timeout=5
        )
        output = result.stdout.strip()
    except subprocess.TimeoutExpired:
        output = "TIMEOUT"
    
    return output, time.time() - start_time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Language argument missing"}))
        sys.exit(1)

    language = sys.argv[1]

    # Читаем код и входные данные из stdin
    data = sys.stdin.read().split("\n", 1)
    code, input_data = data if len(data) == 2 else (data[0], "")

    if language == "cpp":
        output, exec_time = run_cpp_code(code, input_data)
    elif language == "python":
        output, exec_time = run_python_code(code, input_data)
    else:
        output = f"Unsupported language: {language}"
        exec_time = 0

    print(json.dumps({"output": output, "execution_time": exec_time}))