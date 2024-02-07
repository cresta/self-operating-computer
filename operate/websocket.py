import requests
import websocket
import rel
import uuid

class ClientSubscriptionClient():
    def __init__(self):
        self.streamingEndpoint = "wss://api-walter-dev.voice-staging.cresta.ai/ws/v1/clientSubscription/streamMessages"
        self.endpoint = "https://api-walter-dev.voice-staging.cresta.ai/v1/clientSubscription/subscribe"

    def subscribe_topic(self, topics):
        channel = uuid.uuid4().hex
        req = {"channel": channel, "topics": topics}
        response = requests.post(self.endpoint, json=req, auth=("ApiKey", ""))
        resp = response.json()
        return resp

    def stream_messages(self):
        self.ws = websocket.WebSocketApp("wss://api-walter-dev.voice-staging.cresta.ai/ws/v1/clientSubscription/streamMessages",
                                        on_message=self.on_message,
                                        on_error=self.on_error,
                                        on_close=self.on_close)
        self.ws.run_forever(dispatcher=rel, reconnect=5)  # Set dispatcher to automatic reconnection, 5 second reconnect delay if connection closed unexpectedly

    def close(self):
        self.ws.close()
    
    def on_message(self, ws, message):
        print(message)
    
    def on_error(self, ws, error):
        print(error)
    
    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")
