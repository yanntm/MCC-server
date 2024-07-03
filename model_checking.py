import os
import subprocess
import shutil
import hashlib
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import logging
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

logging.basicConfig(level=logging.INFO)

EXAMINATIONS_WITHOUT_XML = ["StateSpace", "OneSafe", "StableMarking", "QuasiLiveness", "Liveness", "ReachabilityDeadlock"]
EXAMINATIONS_WITH_XML = ["UpperBounds", "ReachabilityFireability", "ReachabilityCardinality", "CTLFireability", "CTLCardinality", "LTLFireability", "LTLCardinality"]

def setup_environment(examination, tool, timeout, is_col):
    env = os.environ.copy()
    env['BK_INPUT'] = "MyModel"
    env['BK_EXAMINATION'] = examination
    env['BK_TOOL'] = tool
    env['BK_TIME_CONFINEMENT'] = str(timeout)
    env['BK_MEMORY_CONFINEMENT'] = "16384"
    env['BK_BIN_PATH'] = "/home/mcc/BenchKit/bin/"
    return env

def generate_unique_folder():
    unique_str = f"{time.time()}_{os.getpid()}"
    hash_object = hashlib.sha256(unique_str.encode())
    folder_name = hash_object.hexdigest()[:10]
    run_dir = os.path.join("/home/mcc/BenchKit/run", folder_name)
    os.makedirs(run_dir)
    return run_dir

def run_model_checking(pnml_file, logic_file, examination, tool, is_col, timeout):
    run_dir = generate_unique_folder()
    
    pnml_path = os.path.join(run_dir, 'model.pnml')
    logic_path = os.path.join(run_dir, 'model.logic') if logic_file else None

    # Save the uploaded files to the run directory
    pnml_file.save(pnml_path)
    if logic_file:
        logic_file.save(logic_path)

    if logic_file and examination in EXAMINATIONS_WITH_XML:
        # Run the converter tool
        subprocess.run(['java', '-jar', '/home/mcc/BenchKit/fr.lip6.converter.jar', '-formula', logic_path, '-o', run_dir])
        os.rename(os.path.join(run_dir, 'properties.xml'), os.path.join(run_dir, 'Examination.xml'))

    iscolored_path = os.path.join(run_dir, 'iscolored')
    with open(iscolored_path, 'w') as f:
        f.write("TRUE" if is_col else "FALSE")

    env = setup_environment(examination, tool, timeout, is_col)

    command = [os.path.join(env['BK_BIN_PATH'], '../BenchKit_head.sh')]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, cwd=run_dir, env=env)

    def generate():
        try:
            for stdout_line in iter(process.stdout.readline, ""):
                yield f"data:{stdout_line}\n\n"
            process.stdout.close()
            process.wait()
            for stderr_line in iter(process.stderr.readline, ""):
                yield f"data:{stderr_line}\n\n"
            process.stderr.close()
            yield f"data:Process finished with exit code {process.returncode}\n\n"
        finally:
            shutil.rmtree(run_dir)
            print(f"Cleaned up directory: {run_dir}")

    return Response(generate(), mimetype='text/event-stream')

@app.route('/mcc/<col_flag>/<examination>/<tool>', methods=['POST'])
def mcc_service(col_flag, examination, tool):
    if 'model.pnml' not in request.files:
        return jsonify({'error': 'No model.pnml file provided'}), 400

    pnml_file = request.files['model.pnml']
    logic_file = request.files.get('model.logic')
    is_col = col_flag.upper() == 'COL'
    timeout = request.form.get('timeout', 100, type=int)

    return run_model_checking(pnml_file, logic_file, examination, tool, is_col, timeout)

if __name__ == '__main__':
    logging.info("Starting server...")
    os.makedirs('/home/mcc/BenchKit/run', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
