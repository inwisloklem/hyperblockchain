import time
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-f873c39d-8355-4cbb-894c-591e57988b63"
pnconfig.subscribe_key = "sub-c-59f3e16c-4d03-11ea-814d-0ecb550e9de2"


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f"\nChannel: {message_object.channel}. Message: {message_object.message}")


class PubSub():
    """
    Handle the publish/subscribe layer of the application.
    Provide communication between the nodes of the blockchain network
    """
    def __init__(self, channel, pnconfig=pnconfig):
        self.channel = channel
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels([channel]).execute()
        self.pubnub.add_listener(Listener())

    def publish(self, message):
        """
        Publish the message to the channel
        """
        self.pubnub.publish().channel(self.channel).message(message).sync()


if __name__ == "__main__":
    pubsub = PubSub("TEST_CHANNEL")

    time.sleep(1)
    pubsub.publish({"test": "message"})
