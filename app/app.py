from dependencies import Flask, request, jsonify

app = Flask(__name__)

votes = {"option1": 0, "option2": 0}

@app.route('/')
def home():
    return "Welcome to the Voting App!"

@app.route('/vote', methods=['POST'])
def vote():
    data = request.get_json()
    option = data.get('option')
    if option in votes:
        votes[option] += 1
        return jsonify({"message": "Vote counted!"}), 200
    return jsonify({"message": "Invalid option"}), 400

@app.route('/results', methods=['GET'])
def results():
    return jsonify(votes), 200

if __name__ == "__main__":
    app.run(debug=True)
