from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    # Check for empty or whitespace-only input
    if not msg.strip():
        return jsonify({"error": "Query cannot be empty or whitespace only"}), 400
    print(msg)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])