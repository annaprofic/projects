# pylint: disable=broad-except
"""
Module that allows normalize and denoise text.
"""
import re


def normalize(text: str) -> str:
    """
        Normalizes song names by denoising text and removing punctuation.

        Arguments:
            text (str): text to normalize (songs names)
        Returns:
            text (str): normalized text
    """
    if text:
        try:
            text = remove_between_square_brackets(text)
            text = remove_punctuation(text)
            return text
        except Exception as _:
            print("<",
                  _.__class__.__name__,
                  "> occured, something went wrong with text: '", text, "'")
    else:
        print("We can't process this text.")
        return "Unknown"


def remove_between_square_brackets(text: str) -> str:
    """
        Removes square brackets from text.

        Arguments:
            text (str): text before removing brackets
        Returns:
            text (str): text without square brackets
    """
    return re.sub(r'\[[^]]*\]', '', text)


def remove_punctuation(text: str) -> str:
    """
        Removes punctuation from text.

        Arguments:
            text (str): text before removing punctuation
        Returns:
            text (str): normalized text
    """
    return ' '.join(re.findall(r'\w+', text))
