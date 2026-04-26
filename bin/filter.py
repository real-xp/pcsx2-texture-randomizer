import os

# This file's entire purpose is to generate a new filter.txt file by pointing it to a folder
# It will go through the entire folder's contents and the folders inside that folder too
# It should auto generate a filter file ready for the program

filter_file_list = []
FILTER_PATH = "./test/files/"
ERROR_CODE = '\033[91m'
END_CODE = '\033[0m'

def make_filter_file():
    if (not os.path.exists(FILTER_PATH)):
        print("NOT PATH EXIST")
        return
    try:
        for root, dirs, files in os.walk(FILTER_PATH):
            for n in files:
                fp = os.path.join(root, n)
                ft = fp.replace(FILTER_PATH, "")
                fl = ft.replace("\\", "/")
                if "/" in fl:
                    fl = fl.rsplit('/', 1)[1]
                with open("./filter.txt", 'a') as filter_file:
                    filter_file.write(f"{fl}\n")
    except Exception as error:
        print(f"{ERROR_CODE}[ERROR]\tCould not detect files : {error}{END_CODE}")

make_filter_file()