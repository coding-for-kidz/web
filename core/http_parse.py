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

"""This module parses http headers"""
from enum import Enum


def parse_http_header(request) -> dict:
    """Parses http header string and turns it into a dictionary"""
    lines = request.split("\n")  # splits it into lines
    request_list = []
    request_dict = {}
    for item in lines:
        request_list.append(item.split(": "))
    for item in request_list:
        if item != [""]:
            request_dict[item[0]] = item[1]  # DNT: 1 => ['DNT', 1] => {"DNT", 1}
    return request_dict


class OperatingSystem(Enum):
    Windows_NT = 0
    Windows_Phone = 1
    macOs = 2
    ChromeOs = 3
    Android = 4
    Linux = 5
    ios = 6
    unknown = 7


class UserAgent:
    """The User Agent class interprets the user agent string"""

    def __init__(self, useragent: str):
        self.useragent = useragent

    def useful_useragent(self) -> str:
        """Most browsers impersonate firefox with Mozilla compatibility they have Mozilla/x.y
        at the beginning of their user agent"""
        if "Mozilla/" in self.useragent:
            return str(self.useragent[12 : len(self.useragent)]).lower()
        # Opera does not
        return self.useragent

    def get_browser(self) -> str:
        """Return the browser name"""
        use = self.useful_useragent()
        browser = "unknown"
        if "msie" in use:
            browser = "internet explorer"
        elif ("opera" in use) or ("opr" in use):
            browser = "opera"
        elif ("edge" in use) or ("edg" in use):
            browser = "edge"
        elif "firefox" in use:
            browser = "firefox"
        elif "chrome" in use:
            browser = "chrome"
        elif ("safari" in use) and ("windows" not in use):
            return "safari"
        elif "konqueror" in use:
            browser = "konqueror"
        return browser

    def get_browser_version(self):
        use = self.useful_useragent()
        browser = self.get_browser()
        if browser == "edge":
            browser = "edg"
        if browser == "opera":
            browser = "opr"
        if browser == "unknown":
            return ""
        parts = use.split(" ")
        for item in parts:
            if (browser in item) or ("version" in item):
                parts_of_correct = item.split("/")
                if len(parts_of_correct) > 1:
                    return parts_of_correct[1]
        return ""

    def system(self) -> str:
        """Returns system information"""
        use = (self.useful_useragent().split(")"))[0]
        use = use[1 : len(use)]  # noqa E203
        return use

    def get_os(self) -> OperatingSystem:
        """Returns os"""
        use = self.system()
        operating_system = OperatingSystem.unknown
        if ("windows" in use) and ("phone" not in use):
            operating_system = OperatingSystem.Windows_NT
        elif ("windows" in use) and ("phone" in use):
            operating_system = OperatingSystem.Windows_Phone
        elif "macintosh" in use:
            operating_system = OperatingSystem.macOs
        elif "cros" in use:
            operating_system = OperatingSystem.ChromeOs
        elif "android" in use:
            operating_system = OperatingSystem.Android
        elif "linux" in use:
            operating_system = OperatingSystem.Linux
        elif ("iphone" in use) or ("ipad" in use):
            operating_system = OperatingSystem.ios
        return operating_system

    def get_os_version(self, sec_ch_ua_platform_version="") -> str:
        """
        returns the os version it doesn't include the os name.
        """
        operating_system = self.get_os()
        if operating_system == OperatingSystem.Windows_NT:
            version = str(self.useragent)[24:27]
            switcher = {
                "NT": "NT",
                "XP": "XP",
                "5.0": "2000",
                "5.1": "XP",
                "5.2": "2003",
                "6.0": "Vista",
                "6.1": "7",
                "6.2": "8",
                "6.3": "8.1",
                "10.": "10.0",
                "11.": "11.0",
            }
            v = switcher.get(version, "Invalid Version")
            if (sec_ch_ua_platform_version is not None) and (
                sec_ch_ua_platform_version != "None"
            ):
                if sec_ch_ua_platform_version[0:3] == "15":
                    v = "11.0"
            return v
        if operating_system == OperatingSystem.macOs:
            version = self.system()
            version = version[26 : len(version) - 2]
            cases = {
                "10_0": "Cheetah",
                "10_1": "Puma",
                "10_2": "Jaguar",
                "10_3": "Panther",
                "10_4": "Tiger",
                "10_5": "Leopard",
                "10_6": "Snow Leopard",
                "10_7": "Lion",
                "10_8": "Mountain Lion",
                "10_9": "Mavericks",
                "10_10": "Yosemite",
                "10_11": "El Capitan",
                "10_12": "Sierra",
                "10_13": "High Sierra",
                "10_14": "Mojave",
                "10_15": "Catalina",
                "10_16": "Big Sur",
                "10_17": "Monterey",
                "10_18": "Ventura",
                "11": "Big Sur",
                "12": "Monterey",
                "13": "Ventura",
            }
            return cases.get(version, "Invalid Version")
        return "unknown"

    def is_linux(self) -> bool:
        """Checks if the user runs linux"""
        return self.get_os() == OperatingSystem.Linux

    def get_linux_distro(self):
        """Gets linux distribution"""
        if self.is_linux():
            if "ubuntu" in self.useful_useragent():
                return "ubuntu"
            else:
                return "unknown"
        return False

    def get_architecture(self) -> str:
        """Returns the architecture
        macOS architecture is unknown
        windows architecture is x86, x84-64 or arm
        linux architecture is not implemented
        """
        operating_system = self.get_os()
        use = self.system()
        architecture = "unknown"
        if operating_system == OperatingSystem.Windows_NT:
            if "win64" in use:
                architecture = "x86-64"
            elif "arm" in use:
                architecture = "arm"
            elif "wow64" in use:
                architecture = "x86-64"
            else:
                architecture = "x86"
        return architecture


class HttpHeader:
    """Http Header class"""

    def __init__(self, header, t="str"):
        if t == "str":
            self.header = parse_http_header(header)
        elif t == "dict":
            self.header = header
        else:
            raise TypeError("Invalid type")
        if "User-Agent" in self.header:
            self.user_agent = UserAgent(self.header["User-Agent"])
        if "Accept-Encoding" in self.header:
            self.header["Accept-Encoding"] = self.header["Accept-Encoding"].split(", ")
        if "Accept-Language" in self.header:
            self.header["Accept-Language"] = self.header["Accept-Language"].split(";")
        if "Keep-Alive" in self.header:
            self.header["Keep-Alive"] = int(self.header["Keep-Alive"])
        if "Upgrade-Insecure-Requests" in self.header:
            if self.header["Upgrade-Insecure-Requests"] == "1":
                self.header["Upgrade-Insecure-Requests"] = True
            else:
                self.header["Upgrade-Insecure-Requests"] = False

    def get_user_agent(self) -> UserAgent:
        """Gets the user agent"""
        return self.user_agent

    def get_header(self, header_name: str) -> str:
        """Gets the header"""
        return self.header[header_name]

    def get_header_dict(self) -> dict:
        """Gets the header in dictionary form"""
        return self.header


if __name__ == "__main__":
    f = open("useragents.txt", "r")
    lines = f.read().split("\n")
    for line in lines:
        u = UserAgent(line)
        print(
            line
            + ","
            + u.get_browser()
            + ","
            + u.get_browser_version()
            + ","
            + str(u.get_os())
        )
