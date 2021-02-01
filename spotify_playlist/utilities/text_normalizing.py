import re


def normalize(text: str) -> None:
    """

    :param text:
    :return:
    """
    if text:
        try:
            text = denoise_text(text)
            text = remove_punctuation(text)
            return text
        except Exception as e:
            print("<",
                  e.__class__.__name__,
                  "> occured, something went wrong with text: '", text, "'")
    else:
        print("We can't process this text.")


def remove_between_square_brackets(text: str):
    """

    :param text:
    :return:
    """
    return re.sub(r'\[[^]]*\]', '', text)


def denoise_text(text: str):
    """

    :param text:
    :return:
    """
    text = remove_between_square_brackets(text)
    return text


def remove_punctuation(text: str):
    """
    Remove punctuation from list of tokenized words.
    :param text:
    :return:
    """
    return re.sub(r'[^\w\s]', '', text)
