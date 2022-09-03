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


class Email:
    """Email class"""

    def __init__(self, s):
        self.email_list = s.split("@")
        self.email_name = s[0]
        self.email_provider = s[1]

    def __eq__(self, other):
        if (self.email_name == other.email_name) and (
            self.email_provider == other.email_provider
        ):
            return True
        return False

    def __str__(self):
        return self.email_name + self.email_provider


def check_text_for_email_easy(text):
    text_list = text.replace(" (dot) ", ".")
    text_list = text_list.replace(" ( dot ) ", ".")
    text_list = text_list.replace("(dot)", ".")
    text_list = text_list.replace("( dot )", ".")

    text_list = text_list.replace(" (at) ", "@")
    text_list = text_list.replace(" ( at ) ", "@")
    text_list = text_list.replace("(at)", "@")
    text_list = text_list.replace("( at )", "@")

    text_list = text_list.split(" ")
    emails = []
    for item in text_list:
        if ("@" in item[1 : len(item)]) and ("." in item) and ("\n" not in item):
            emails.append(Email(item))
    return emails


def check_for_emails(text: str) -> list:
    text = text.lower()
    return check_text_for_email_easy(text)
