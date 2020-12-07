import re


def normalize(word):
    word = denoise_text(word)
    word = remove_punctuation(word)
    return word


def remove_between_square_brackets(text):
    return re.sub(r'\[[^]]*\]', '', text)


def denoise_text(text):
    text = remove_between_square_brackets(text)
    return text


def remove_punctuation(word):
    """Remove punctuation from list of tokenized words"""
    return re.sub(r'[^\w\s]', ' ', word)
