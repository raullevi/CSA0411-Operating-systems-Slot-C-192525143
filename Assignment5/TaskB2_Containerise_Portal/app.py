from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample university result database
STUDENT_RESULTS = {
    "192525143": {"name": "Rakul K", "course": "CSA0411 Operating Systems", "grade": "O", "gpa": 9.85},
    "192525144": {"name": "Arun V", "course": "CSA0411 Operating Systems", "grade": "A+", "gpa": 9.20},
    "192525145": {"name": "Priya S", "course": "CSA0411 Operating Systems", "grade": "O", "gpa": 9.90}
}

@app.route("/")
def home():
    return jsonify({
        "portal": "SIMATS University Semester Result Portal",
        "status": "online",
        "version": "1.0.0"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/result/<reg_no>")
def get_result(reg_no):
    result = STUDENT_RESULTS.get(reg_no)
    if result:
        return jsonify({"success": True, "data": result})
    return jsonify({"success": False, "error": "Register number not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
