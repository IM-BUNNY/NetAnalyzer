from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    source = data['source']
    destination = data['destination']
    logger.debug(f"Received request: source={source}, destination={destination}")

    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        executable_name = "pathfinder.exe" if os.name == "nt" else "pathfinder"
        executable_path = os.path.join(current_dir, executable_name)

        if not os.path.exists(executable_path):
            logger.error(f"C++ executable not found at: {executable_path}")
            return jsonify({"error": f"C++ executable '{executable_name}' not found at {executable_path}. Please compile pathfinder.cpp."}), 500

        if os.name != "nt":
            os.chmod(executable_path, 0o755)
            logger.debug(f"Set execute permissions for {executable_path}")

        logger.debug(f"Running C++ executable: {executable_path}")
        process = subprocess.run(
            [executable_path],
            input=f"{source}\n{destination}\n",
            text=True,
            capture_output=True,
            timeout=10
        )

        logger.debug(f"C++ program output: stdout={process.stdout}, stderr={process.stderr}, returncode={process.returncode}")

        if process.returncode != 0:
            logger.error(f"C++ program failed: {process.stderr}")
            return jsonify({"error": f"C++ program failed: {process.stderr}"}), 500

        output = process.stdout.strip().split('\n')

        if "No path exists" in output[0] or "Invalid node" in output[0]:
            logger.warning(f"Pathfinding error: {output[0]}")
            return jsonify({"error": output[0]}), 400
        
        path_line = output[0].replace("Shortest path: ", "").split(" -> ")
        distance = float(output[1].replace("Total distance: ", "").replace(" km", ""))
        logger.debug(f"Parsed path: {path_line}, distance: {distance}")
        
        return jsonify({"path": path_line, "distance": distance})
    except subprocess.TimeoutExpired:
        logger.error("C++ program timed out after 10 seconds")
        return jsonify({"error": "C++ program timed out after 10 seconds"}), 500
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)