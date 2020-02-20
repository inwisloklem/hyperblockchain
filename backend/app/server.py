import os
import requests
from flask import Flask, jsonify
from backend.blockchain.blockchain import Blockchain
from backend.blockchain.errors import BlockchainReplacementError
from backend.pubsub import BLOCK_CHANNEL, DEFAULT_CHANNEL, PubSub
from backend.util.generate_port import generate_port

DEFAULT_PORT = 4444
TRANSACTION_DATA = 'stubbed transaction data'

blockchain = Blockchain()
pubsub = PubSub([BLOCK_CHANNEL, DEFAULT_CHANNEL], blockchain)

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

is_peer = os.environ.get("PEER") == "True"


@app.route("/blockchain")
def get_blockchain():
    return jsonify(blockchain.to_json())


@app.route("/blockchain/mine")
def get_blockchain_mine():
    blockchain.add_block(TRANSACTION_DATA)
    block = blockchain.get_last_block()
    pubsub.broadcast_block(block)

    return jsonify(block.to_json())


def synchronize():
    if is_peer:
        response = requests.get(f"http://127.0.0.1:{DEFAULT_PORT}/blockchain")
        chain_json = response.json()

        try:
            blockchain.replace_chain(Blockchain.from_json(chain_json))
            print("Synchronization success\n")
        except BlockchainReplacementError as e:
            print(f"Synchronization failure: {e}\n")


synchronize()
app.run(port=generate_port(is_peer, DEFAULT_PORT))
