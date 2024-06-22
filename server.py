from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import subprocess
import os
import logging
from status import list_tools, list_examinations, get_all_tools_and_examinations
from model_checking import mcc_service

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

logging.basicConfig(level=logging.INFO)

@app.route('/run', methods=['POST'])
def run_model_checker():
    if 'model.pnml' not in request.files:
        return jsonify({'error': 'No model.pnml file provided'}), 400

    model_file = request.files['model.pnml']
    model_file.save('run/model.pnml')

    def generate():
        command = ['./run_tool.sh', 'run/model.pnml']
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for stdout_line in iter(process.stdout.readline, ""):
            yield f"data:{stdout_line}\n\n"
        process.stdout.close()
        process.wait()
        yield f"data:Process finished with exit code {process.returncode}\n\n"

    return Response(generate(), mimetype='text/event-stream')

@app.route('/tools/list', methods=['GET'])
def get_tools():
    tools = list_tools()
    return jsonify({'tools': tools})

@app.route('/tools/<tool>/examinations', methods=['GET'])
def get_examinations(tool):
    examinations = list_examinations(tool)
    return jsonify(examinations)

@app.route('/tools/descriptions', methods=['GET'])
def get_all_tools_and_examinations_route():
    tools_info = get_all_tools_and_examinations()
    return jsonify({'tools_info': tools_info})

# Add the new MCC service route
app.add_url_rule('/mcc/<col_flag>/<examination>/<tool>', view_func=mcc_service, methods=['POST'])

if __name__ == '__main__':
    logging.info("Starting server...")
    os.makedirs('run', exist_ok=True)
    app.run(host='0.0.0.0', port=5000)
