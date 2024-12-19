import re


def basic_cleaner(text):
    text = re.sub(r'\n\s+', '\n', text)
    text = re.sub(r'^\s+', '', text)
    text = re.sub(r'\s+$', '', text)
    return text


def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"# emoticons  
                           u"\U0001F300-\U0001F5FF"# symbols & pictographs
                           u"\U0001F680-\U0001F6FF"# transport & map symbols  
                           u"\U0001F1E0-\U0001F1FF"# flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def english_text_preprocess(string):
    string = remove_emoji(string).strip()
    return string