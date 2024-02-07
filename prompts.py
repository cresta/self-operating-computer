def google_search_action(q: str)->str:
    return f'''
        Open Chrome and search the following question in the search bar:
        {q}
        Click the first result which is not an advertisement.
    '''
    
def summarize_conversation(conv: str)->str:
    return f'''
        Please summarize the following conversation:
        {conv}
        Open google docs and write the summary into it.
    '''    
