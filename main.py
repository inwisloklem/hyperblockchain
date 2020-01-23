from backend.blockchain.blockchain import Blockchain

if __name__ == "__main__":
    blockchain = Blockchain()

    blockchain.add_block("second block data")
    blockchain.add_block("third block data")

    print(blockchain)
