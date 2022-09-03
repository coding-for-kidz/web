"""Compiles css so that it is smaller and takes up less bandwidth"""
from os import listdir, getcwd, path
from os.path import isfile, join


def compile_css(text):
    """Compile css"""
    list_text = text.split("\n")
    text = ""
    for line in list_text:
        stripped_line = line.strip(" ")
        if stripped_line[0:2] != "/*":
            text += line + "\n"
    text.replace("\t", "")
    text.replace("    ", "")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.replace("\n", "  ")

    return text


def add_and_compile_css(file_list):
    compiled_css = []
    for item in file_list:
        file = open(css_path + item, "r", encoding="UTF-8")
        compiled_css.append(compile_css(file.read()))
        file.close()
    return combine_compiled_css(compiled_css)


def combine_compiled_css(compiled_files):
    """Combine multiple files that have been compiled"""
    compiled = ""
    for item in compiled_files:
        compiled += item + "  "
    return compiled


def get_file_list(css_path):
    return [f for f in listdir(css_path) if isfile(join(css_path, f))]


# file paths
css_path = "../css/"  # /frontend/css
loose_files_css_path = css_path + "loose_files/"  # /css/loose_files/

# file lists
file_list = get_file_list(css_path)
loose_files_list = [
    f for f in listdir(loose_files_css_path) if isfile(join(loose_files_css_path, f))
]

# print file lists
for file in file_list:
    print("Found: " + file)

for file in loose_files_list:
    print("Found Loose File: " + file)

# compiled css path
cwd = getcwd()
compiled_css_path = cwd[0 : len(cwd) - 14] + "\\website\\static\\css\\"

# compiled css temp storage
compiled_css = add_and_compile_css(file_list)

# loose files
loose_files_compiled = {}

for item in loose_files_list:
    loose_file = open(loose_files_css_path + item, "r", encoding="UTF-8")
    loose_files_compiled[item] = compile_css(loose_file.read())
    loose_file.close()

print("\nWriting to bundle.min.css at " + compiled_css_path)
bundle_file_w = open(compiled_css_path + "bundle.min.css", "w", encoding="UTF-8")
bundle_file_w.write(compiled_css)
bundle_file_w.close()
print(
    "Bundle Size: "
    + str(path.getsize(compiled_css_path + "bundle.min.css"))
    + " bytes\n"
)
print("\n")

for key in loose_files_compiled:
    print("Writing to " + key + " at " + compiled_css_path)
    loose_file = open(compiled_css_path + key, "w", encoding="UTF-8")
    loose_file.write(loose_files_compiled[key])
    loose_file.close()
    print("File Size: " + str(path.getsize(compiled_css_path + key)) + " bytes\n")
