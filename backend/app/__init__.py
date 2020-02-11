from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain

blockchain = Blockchain()

for i in range(4):
    blockchain.add_block(f"block {i}")

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/blockchain")
def get_blockchain():
    return jsonify(blockchain.to_json())


app.run(port=4444)
