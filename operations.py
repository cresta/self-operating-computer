from operate.main import main
from operate.models.apis import extract_entities

def take_notes_in_google_docs(notes: str):
    print(f'summary: {notes}')
    prompt = f"Open google docs with a new doc. Input \"{notes}\", and then change title to \"Notes\". And then save it"
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)

def google_search(q: str):
    prompt = f"Chrome app is already opened on the desktop, please create a new tab, and search {q} in the search bar"
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)

def add_authorized_user(message_list):
    entities = extract_entities(message_list)
    print(entities)
    prompt = "Open the google spreadsheet https://docs.google.com/spreadsheets/d/1sRPnpL-vPQXqwtKefN0O51jyCYSCKZIuFY6OT6CIqCM/edit#gid=0, then" + f" click ### and input {entities['new_user']}." + " Close the spreadsheet after finishing it."
    print(prompt)
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)