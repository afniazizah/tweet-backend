def case_folding(text):
    if isinstance(text, str):
      lowercase_text = text.lower()
      return lowercase_text
    else:
      return text
def case_folding_tweet(data):
    data['case_folding'] = data['cleaning'].apply(case_folding)
    return data