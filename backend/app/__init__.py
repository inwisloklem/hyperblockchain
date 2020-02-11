from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from pydash import last

TRANSACTION_DATA = 'stubbed transaction data'

blockchain = Blockchain()

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/blockchain")
def get_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def get_blockchain_mine():
    blockchain.add_block(TRANSACTION_DATA)
    return jsonify(last(blockchain.chain).to_json())


app.run(port=4444)
