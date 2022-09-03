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
"""Testcode implementation"""
from flask import Blueprint, render_template, redirect

from services.web.website import cache

testcode = Blueprint("testcode", __name__)


@testcode.route("/code/<string:lang>/", endpoint="test_code")
@cache.cached(1000000)
def test_code(lang: str):
    redirect_map = {
        "py": "python",
        "js": "javascript",
        "ts": "typescript",
        "rb": "ruby",
        "cplusplus": "c++",
        "csharp": "c#",
        "node": "nodejs",
        "md": "markdown",
    }
    example_code = {
        "javascript": "alert('Hello ' + 'World')\n",
        "java": "System.out.println('Hello ' + 'World')\n",
        "css": "p {\n\tcolor: red\n}\n",
        "markdown": "#Test\ntest\n",
        "php": "echo 'Hello ' . 'World'\n",
        "nodejs": 'console.log("hello"+" world")\n',
        "shell": 'echo "Hello World"\n',
        "ruby": "puts 'Hello World'\n",
        "c": "printf('Hello World')\n",
        "c++": "int main()\n{\n\tprintf('Hello World');\nreturn 0;\n",
        "go": "package main\n\nimport \"fmt\"\n\nfunc main()\n{\n  fmt.Println('Hello World')\n}\n",
        "swift": "print('Hello World')\n",
        "rust": "print!('Hello World', \"{}\")\n",
        "scala": "println('Hello World')\n",
        "elixir": "def main()\n{\n  print('Hello World')\n}\n",
        "c#": "using System;\n\nclass HelloWorld\n{\n\tstatic void Main() {\n\tConsole.WriteLine('Hello World')\n}\n}"
        "\n",
    }
    if lang in redirect_map:
        return redirect("/code/" + redirect_map[lang], 301)
    try:
        if (lang != "python") and (lang != "html"):
            return render_template(
                "code_langs/run-code-temp.jinja",
                language=lang,
                example_code=example_code[lang],
            )
        elif lang == "python":
            return render_template("code_langs/run-code-python.jinja")
        else:
            return render_template("code_langs/run-code-html.jinja")
    except KeyError:
        return render_template(
            "code_langs/run-code-temp.jinja", language=lang, example_code=""
        )


@testcode.route("/code/<string:lang>/iframe/", endpoint="iframe_code")
def iframe_code(lang: str):
    if lang == "python":
        return render_template("code_langs/iframe/run-code-python.jinja")
    elif lang == "html":
        return render_template("code_langs/iframe/run-code-html.jinja")
    return render_template(
        "code_langs/iframe/run-code-temp.jinja", language=lang, example_code=""
    )
