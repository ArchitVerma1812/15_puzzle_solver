from flask import Flask, render_template, request, jsonify
import heapq
import os
from werkzeug.utils import secure_filename
import astar  # Importing the A* module

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

# A* algorithm solver route
@app.route("/solve", methods=["POST"])
def solve():
    start_puzzle = request.json["puzzle"]  # Start puzzle is received from frontend
    goal_puzzle = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]
    path = astar.a_star_15_puzzle(start_puzzle, goal_puzzle)  # Use the A* function from astar.py
    if path:
        return jsonify({"solution": path, "moves": len(path) - 1})
    return jsonify({"solution": None, "error": "No solution found"})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload_image", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)
    
    return jsonify({"image_path": file_path})

if __name__ == "__main__":
    app.run(debug=True)
