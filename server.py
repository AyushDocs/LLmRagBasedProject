from flask import Flask, request, jsonify
import uvicorn
from Rag.ProblemSolver import solve
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def get_endpoint():
    data= request.get_json()
    response=solve(data)
    return jsonify({"message": f"Received query parameter: {response}"}), 200

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)