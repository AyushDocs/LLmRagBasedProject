from flask import Flask, request, jsonify
import uvicorn
from Project.ProblemSolver import solve
from Project.Initializer import init
import os
import dotenv

dotenv.load_dotenv()

# init()
app = Flask(__name__)


@app.route('/api', methods=['POST'])
def get_endpoint():
    data= request.get_json()
    if (request.files):
        file=request.files["file"]
        UPLOAD_FOLDER = "uploads"
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        file.save(file_path)
        if(file):
            current_file_path = os.path.abspath(__file__)
        response=solve(data,current_file_path)
        os.remove(file_path)
    else:
        response=solve(data)

    return jsonify(response), 200

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    # uvicorn.run(app, host="0.0.0.0", port=8000)