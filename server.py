from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
from operate.main import main
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
cors = CORS(app)

thread_pool = ThreadPoolExecutor(max_workers=1)

def handler(body):
    pass

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
    thread_pool.submit(handler, body)
    return {}, HTTPStatus.OK

@app.post("/conversationEvents")
def postConversationEvents():
    body = request.json
    print(body)
    thread_pool.submit(handler, body)
    return {}, HTTPStatus.OK