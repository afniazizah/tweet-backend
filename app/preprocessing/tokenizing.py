def tokenizing(text):
    tokens = text.split()
    return tokens

def tokenizing_tweet(data):
    data['tokenizing'] = data['case_folding'].apply(tokenizing)
    return data
