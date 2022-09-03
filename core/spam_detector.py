#  Copyright 2021 Coding for Kidz Project
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Spam detector"""


def shorten_word(word: str) -> str:
    """Shortens text"""
    new_text = ""
    previous = " "
    exceptions = ["hit", "hello"]
    if word in exceptions:
        return word
    for item in word:
        if item not in "aeiou":
            new_text += item
        elif previous == " ":
            new_text += item
        previous = item
    return new_text


def shorten_text(text: str):
    """
    Shortens text
    """
    text = text.split("\n")
    new_text = []
    for item in text:
        new_text.append(shorten_word(item))
    return new_text


def spam_detector(text: str) -> bool:
    """Detects spam"""
    text = text.lower()
    text = text.split(" ")
    rude_words = ["scks", "sck", "hell", "damm", "damn"]
    for word in text:
        for item in rude_words:
            if item in shorten_text(word):
                return True
            if item in text:
                return True

    same = 0
    previous = ""
    for item in text:
        if item == previous:
            same += 1
        else:
            same = 0
    if same >= 6:
        return True
    return False
