import cbpro, time

from utilities.secrets import Secrets


class MyWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.message_count = 0
        self.latest_msg = None
    def on_message(self, msg):
        self.message_count += 1
        if self.channels[0]['name'] == "ticker":
            if 'price' in msg:
                self.latest_msg = float(msg['price'])
    def on_close(self):
        print("-- Closing websocket connection --")
