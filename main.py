'''
XP's Texture Randomiser Script
'''

import os
import random
import datetime

# variables global

TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)
SEED = "" # PUT YOUR SEED HERE, wait that sounds wrong, i mean PUT THE SEED FOR THE RANDOMISER HERE
SOURCE_PATH = "./textures/" # This is the path for source textures
FINAL_PATH = "./replacements/" # this is the path where all textures will be moved

# testing if filelist can even be detected
try:
    file_list = os.listdir(path=SOURCE_PATH)
except:
    print("\n---\tError Detecting Files\t---\n")

extension_file_array = {}

# this function does exactly that
def get_file_list():
    # filter files
    try:
        with open("./filter.txt", 'r') as filter_file:
            filter_file_list = [line.strip() for line in filter_file]
    except:
        print("\n---\tFilter File Could Not Be Loaded!\t---\n")

    for file in file_list: # for loop to loop through files
        try:
            file_name, extension = os.path.splitext(file) # splits filename and extension
        except:
            print("\n---\tError Detecting Files!\t---\n")
            continue

        if (file_name not in filter_file_list):
            if (extension != ''): # checks if somehow extension does not exist
                if (extension_file_array.get(extension) != None): # checks if there is an existing key value entry in dictionary
                    temp_list_array = extension_file_array[extension] # gets the list of files of that particular extension type
                    temp_list_array.append(file_name) # adds current iteration file name into that list
                else:
                    extension_file_array.update({extension : [file_name]}) # makes a new key value pair and adds it to dict

# checks validity of path, -1 = error, 0 = passed check
def check_path_validity():
    if (os.path.exists(SOURCE_PATH)):
        print("\n---\tSource Path Valid\t---\n")
        if (os.path.exists(FINAL_PATH)):
            print("\n---\tFinal Path Valid\t---\n")
            return 0
        else:
            print("\n---\tFinal Path Invalid. Making New Folder Based On Path\t---\n")
            try:
                os.mkdir(FINAL_PATH)
                return 0
            except:
                print("\n---\tError Making Folder For Final Path\t---\n")
                return -1
    else:
        print("\n---\tSource Path INVALID\t---\n")
        return -1

# rename files of specific extension
def rename_spec_ext():
    if (not extension_file_array):
        print("\n---\tFile Replacements Not Possible. No Files Detected!\t---\n")
    else:
        for extension, value_list in extension_file_array.items(): # loop through list, giving extension, value of extension in dict
            randomised_list = value_list.copy() # copy into randomised list
            random.shuffle(randomised_list) # shuffles

            for index, file_name in enumerate(value_list):
                try:
                    original_file_path = os.path.join(SOURCE_PATH, file_name+extension)
                    # renamed_file_path = os.path.join(FINAL_PATH, file_name+" to "+randomised_list[index]+extension) TEST 
                    renamed_file_path = os.path.join(FINAL_PATH, randomised_list[index]+extension)

                    log_text = f"Renaming {original_file_path} to {renamed_file_path}"
                    print (log_text)
                    log_text_write(log_text)
                    os.rename(original_file_path, renamed_file_path)
                except:
                    print("\n---\tError Renaming And Moving File From Source To Final Path\t---\n")
        print("\n---\tFile Replacements Done!\t---\n")

# crypto miner, jk, this just notes the seeds in the seeds.txt file with timestamps
def seed_txt(seed_file):
    seed_file = open("./seeds.txt", "a")
    seed_file.write(f"{TIMESTAMP} -> {seed_file}\n")
    seed_file.close()

def log_txt_initialize():
    log_file = open("./log.txt", "a")
    log_file.write(f"\n------{TIMESTAMP}------\n\n")
    log_file.close()

def log_text_write(string_file):
    log_file = open("./log.txt", "a")
    log_file.write(f"{string_file}\n")
    log_file.close()

# ---
# Main Function
def main():

    if (SEED != ''):
        random.seed(SEED)
        seed_txt(SEED)
    else:
        random.seed(str(TIMESTAMP.timestamp()))
        seed_txt(str(TIMESTAMP.timestamp()))

    if (check_path_validity() == 0):
        log_txt_initialize()
        get_file_list()
        rename_spec_ext()
    else:
        print("\n---\tExiting Program!\t---\n")

main()