from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
from operate.main import main
from concurrent.futures import ThreadPoolExecutor
from operate.models.apis import summarize_messages

app = Flask(__name__)
cors = CORS(app)

thread_pool = ThreadPoolExecutor(max_workers=1)

messages = []
conversation_events = []

def handleConversationEvent(body):
    conversation_events.append(body)
    type = body.get('type', None)
    if type and type == 'CLOSE':
        summary = summarize_messages(messages)
        print(summary)
        messages.clear()
        conversation_events.clear()

def handleMessage(msg):
    messages.append(msg)
    text = msg.get('text', None)
    if text and 'credit score' in text and '?' in text:
        prompt = 'What is my credit score?'
        main(model="gpt-4-with-ocr", terminal_prompt=prompt)

@app.route('/')
def hello():
    return '<h1>This is a self-operating computer</h1>'


@app.route('/health', methods=['GET'])
def health():
    return 'I am healthy!', HTTPStatus.OK

@app.route('/operate', methods=['POST'])
def operate():
    body = request.json
    if not body:
        raise Exception('Request body is empty.')
    prompt = body.get('prompt', None)
    if not prompt:
        return {'error': 'prompt is required'}, HTTPStatus.BAD_REQUEST
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)
    return {}, HTTPStatus.OK


@app.post("/messages")
def postMessages():
    body = request.json
    print(body)
    thread_pool.submit(handleMessage, body)
    return {}, HTTPStatus.OK

@app.post("/conversationEvents")
def postConversationEvents():
    body = request.json
    print(body)
    thread_pool.submit(handleConversationEvent, body)
    return {}, HTTPStatus.OK