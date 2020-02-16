import time
from backend.blockchain.block import Block
from backend.blockchain.errors import BlockchainReplacementError
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-f873c39d-8355-4cbb-894c-591e57988b63"
pnconfig.subscribe_key = "sub-c-59f3e16c-4d03-11ea-814d-0ecb550e9de2"

BLOCK_CHANNEL = "BLOCK_CHANNEL"
DEFAULT_CHANNEL = "DEFAULT_CHANNEL"


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(f"\nChannel: {message_object.channel}. Message: {message_object.message}")

        if message_object.channel == BLOCK_CHANNEL:
            block = Block.from_json(message_object.message)
            potential_chain = self.blockchain.chain[:]
            potential_chain.append(block)

            try:
                self.blockchain.replace_chain(potential_chain)
                print(f"\nSuccess. Replaced the local chain")
            except BlockchainReplacementError as e:
                print(f"\nFailure. Can't replace the local chain: {e}")


class PubSub():
    """
    Handle the publish/subscribe layer of the application.
    Provide communication between the nodes of the blockchain network
    """
    def __init__(self, channels, blockchain, pnconfig=pnconfig):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(channels).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(BLOCK_CHANNEL, block.to_json())

    def publish(self, channel, message):
        """
        Publish the message to the channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()


if __name__ == "__main__":
    pubsub = PubSub([DEFAULT_CHANNEL])

    time.sleep(1)
    pubsub.publish(DEFAULT_CHANNEL, {"test": "message"})
