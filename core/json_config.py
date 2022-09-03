"""Parses the json config"""


class JsonConfig:
    file = ""
    parse = []
    path = ""

    def __init__(self, path=None, text=None):
        if path is not None:
            self.file = open(path, "r").read()
            self.path = path
        else:
            self.file = text
        self.file.replace("\t", "")
        keys = self.file.split(",")
        parse = keys
        for key_value in parse:
            key_value_pair = key_value.split(":")
            key_value_pair[0] = key_value_pair[0].split('"')[1]
            value = key_value_pair[1].split('"')[1]

            if value == "true":
                value = True
            elif value == "false":
                value = False

            key_value_pair[1] = value

            self.parse.append(key_value_pair)

    def get(self, key):
        for key_value in self.parse:
            if key_value[0] == key:
                return key_value[1]

        raise KeyError("Key does not exist")

    def set(self, key, value):
        for key_value in self.parse:
            if key_value[0] == key:
                key_value[1] = value

    def write(self):
        if self.path == "":
            raise ImportError
        else:
            to_write = "{\n"
            for key_value_pair in self.parse:
                to_write += (
                    '\t"'
                    + key_value_pair[0]
                    + '": "'
                    + str(key_value_pair[1])
                    + '", \n'
                )
            to_write = to_write[0 : len(to_write) - 3]  # noqa E203
            to_write += "\n}"
            f = open(self.path, "w")
            f.write(to_write)
