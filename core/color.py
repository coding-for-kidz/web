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
"""Allows for the coloring of print statements"""
import cython

ENDF = "\033[0m"
BOLD = "\033[1m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BGGREY = "\033[7m"

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
DARKYELLOW = "\033[33m"
SKYBLUE = "\033[34m"
PURPLE = "\033[35m"
TEAL = "\033[36m"
GREY = "\033[37m"

BGBLACK = "\033[40m"
BGRED = "\033[41m"
BGGREEN = "\033[42m"
BGDARKYELLOW = "\033[43m"
BGSKYBLUE = "\033[44m"
BGPURPLE = "\033[45m"
BGTEAL = "\033[46m"
BGGREY = "\033[47m"

GREY2 = "\033[90m"
FAIL = "\033[91m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
OKBLUE = "\033[94m"
HEADER = "\033[95m"
OKCYAN = "\033[96m"
WHITE = "\033[97m"


@cython.compile
def color_text(text, color) -> str:
    """Simple way to color text"""
    return color + text + "\033[0m"
