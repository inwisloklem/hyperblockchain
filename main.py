from backend.blockchain.blockchain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_block("second block data")
    blockchain.add_block("third block data")
    blockchain.add_block("fourth block data")
    blockchain.add_block("fifth block data")

    print(blockchain)
