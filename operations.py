from operate.main import main


def take_notes_in_google_docs(notes: str):
    prompt = f"Open google docs with a new doc. Input \"{
        notes}\" Change title to \"Notes\". Close after saving it."
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)


def google_search(q: str):
    prompt = f"Chrome app is already opened on the desktop, please create a new tab, and search {
        q} in the search bar"
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)
