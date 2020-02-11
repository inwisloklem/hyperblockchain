import time
from pubnub.callbacks import SubscribeCallback
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

TEST_CHANNEL = "TEST_CHANNEL"


class Listener(SubscribeCallback):
    def message(self, pubnub, message_object):
        print(f"\nMessage object: {message_object}")


pnconfig = PNConfiguration()
pnconfig.publish_key = "pub-c-f873c39d-8355-4cbb-894c-591e57988b63"
pnconfig.subscribe_key = "sub-c-59f3e16c-4d03-11ea-814d-0ecb550e9de2"

pubnub = PubNub(pnconfig)
pubnub.subscribe().channels(TEST_CHANNEL).execute()
pubnub.add_listener(Listener())

if __name__ == '__main__':
    time.sleep(1)
    pubnub.publish().channel(TEST_CHANNEL).message({"test": "message"}).sync()
