from flask import Flask, request, jsonify
from Project.ProblemSolver import solve
import os
import dotenv
import uvicorn

# Load environment variables
dotenv.load_dotenv()

UPLOAD_DIR = "uploads"
app = Flask(__name__)

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
ROOT_DIR = os.path.dirname(__file__)


@app.route('/')
def home():
    return 'Hello World'
@app.route('/api', methods=['POST'])
def endpoint():
    question = request.form.get("question")

    # Ensure a valid question is provided
    if not question:
        return jsonify({"error": "Missing 'question' parameter"}), 400

    file_path = None
    try:
        print(_file_has_been_uploaded(request))
        print(request.files)
        print(request.form)
        if _file_has_been_uploaded(request):
            file = request.files.get('file')
            file_path = _save_file_and_get_path(file)

        # Call the solve function
        response = solve(question, ROOT_DIR, file_path)

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Ensure file cleanup
        if file_path and os.path.exists(file_path):
            # os.remove(file_path)
            pass

def _save_file_and_get_path(file):
    file_path = os.path.join(ROOT_DIR, UPLOAD_DIR, file.filename)
    file.save(file_path)
    return file_path

def _file_has_been_uploaded(user_request):
    return "file" in user_request.files and user_request.files.get("file").filename != ""

if __name__ == "__main__":
   uvicorn.run(app, host="0.0.0.0", port=5000)
