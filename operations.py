import json
from operate.main import main
from operate.models.apis import extract_entities


def take_notes_in_google_docs(notes: str):
    print(f'summary: {notes}')
    prompt = f"Open Chrome using Spotlight search and open a new google docs. Input \"{notes}\", and then change title to \"Notes\". And then save it"
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)


def google_search(q: str):
    prompt = f"Chrome app is already opened on the desktop, please create a new tab, and search {q} in the search bar"
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)


def add_authorized_user(message_list):
    entities = extract_entities(message_list)
    print("abc extracted entities: ", entities)
    entities = json.loads(entities)
    prompt = "Open Chrome using Spotlight search and go to the google spreadsheet at https://docs.google.com/spreadsheets/d/1sRPnpL-vPQXqwtKefN0O51jyCYSCKZIuFY6OT6CIqCM/edit#gid=0." + f" Click the cell filled with AAA, input {entities['new_user']}, and press enter." + " Close the spreadsheet after finishing it."
    print("prompt: ", prompt)
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)
