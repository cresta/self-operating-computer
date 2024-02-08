from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
from operate.main import main
from concurrent.futures import ThreadPoolExecutor
from operate.models.apis import summarize_messages
from datetime import datetime
from operations import add_authorized_user, take_notes_in_google_docs

app = Flask(__name__)
cors = CORS(app)

thread_pool = ThreadPoolExecutor(max_workers=1)

messages = {}
conversation_events = []


def handleConversationEvent(body):
    conversation_events.append(body)
    type = body.get('type', None)
    if type and type == 'CLOSE':
        message_list = sorted(messages.values(), key=lambda item: item['create_time'])
        print(f'message list: {message_list}')
        summary = summarize_messages(message_list)
        take_notes_in_google_docs(summary)
        print(summary)
        messages.clear()
        conversation_events.clear()


def handleMessage(msg):
    if not validateMessage(msg):
        return
    create_time_str = msg['createTime']
    try:
        create_time = parse_timestamp(create_time_str)
    except ValueError:
        print(f'Invalid timestamp format {create_time_str}. Please use YYYY-MM-DDTHH:mm:ss.mmm.')
    
    name = msg['name']
    text = msg['text']
    speaker = msg.get('speaker', None)
    messageExists = messages.get(name, None)
    messages[name] = {'name': name, 'text': text, 'speaker': speaker, 'create_time': create_time}
    text = msg.get('text', None)
    if not messageExists and text and 'handle it for you' in text.lower():
        message_list = sorted(messages.values(), key=lambda item: item['create_time'])
        print(f'message list: {message_list}')
        add_authorized_user(message_list=message_list)


def parse_timestamp(ts):
    return datetime.fromisoformat(ts.replace('Z', '+00:00'))


def validateMessage(message):
    if message is None:
        return False
    if message.get('name', None) is None:
        return False
    if message.get('text', None) is None:
        return False
    if message.get('createTime', None) is None:
        return False
    return True


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
