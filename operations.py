from operate.main import main

def take_notes_in_google_docs(notes: str):
    prompt = f"Open google docs with a new doc. Input \"{notes}\" Change title to \"Notes\". Close after saving it."
    main(model="gpt-4-with-ocr", terminal_prompt=prompt)