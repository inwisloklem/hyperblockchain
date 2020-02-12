import os
import random
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.pubsub import PubSub
from pydash import last

DEFAULT_PORT = 4444
TRANSACTION_DATA = 'stubbed transaction data'

blockchain = Blockchain()
pubsub = PubSub("DEFAULT_CHANNEL")

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/blockchain")
def get_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def get_blockchain_mine():
    blockchain.add_block(TRANSACTION_DATA)
    return jsonify(last(blockchain.chain).to_json())


def generate_port(is_peer, min_port=4444, max_port=8888):
    """
    Generate port number from `min_port` to `max_port` if in peer mode.
    Else use default port number
    """
    return random.randint(min_port, max_port) if is_peer else DEFAULT_PORT


is_peer = os.environ.get("PEER") == "True"
app.run(port=generate_port(is_peer))
