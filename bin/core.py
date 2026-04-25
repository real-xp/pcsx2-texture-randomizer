import os
import random
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
import json
import shutil
import variables
import app

# ------------------------------------------------------------
#                       CORE FUNCTION
# ------------------------------------------------------------

# This is the array that stores the file names including their paths
# This is mainly for temproary reasons to check if the source folder has image files
file_list = []                                              # empty dict initialised before

# This is a dict / map for the files
# The key is the extension for the file
# The value is the path of the file of that particular extension
# This can be used to filter out particular extensions too
extension_file_dict = {}                                   # empty dict initialised before

# this function does exactly that
def get_file_list(files : list):

    # This is the variable that stores the temproary data for the file names in the filter.txt file
    # This should contain data like `91fea45880122683-9788124e782590b3-00005994`, it should remove extensions from the names
    filter_file_list = []

    try:
        with open("./filter.txt", 'r') as filter_file:             
            for line in filter_file:                                            # parses lines from filter.txt to the array
                line.strip()                                                    # removes newline character
                if (line.find(".") != -1):
                    filter_file_list.append(line.rsplit('.', 1)[0])             # removes the extension
    except Exception as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tCould not detect filter file : {error}{variables.END_CODE}")
        showwarning(title="Filter List", message="Filter List Not Found", detail="Filter List was not found or does not exist.")

    # Checks and splits filename and extension from the retrieved file_list
    for file in files:                                                          # for loop to loop through files
        try:
            file_name, extension = os.path.splitext(file)                       # splits filename and extension
        except Exception as error:
            print(f"{variables.ERROR_CODE}[ERROR]\tCould not separate file name from extension : {error}{variables.END_CODE}")
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
            continue

        file_is_in_filter = False                                               # filter bool
        for filter_element in filter_file_list:                                 # checks if filename is in filter
            if filter_element in file_name:
                file_is_in_filter = True
                break

        if (file_is_in_filter):                                                 # checks if file is in filter list
            continue

        if (extension != ''):                                                   # checks if somehow extension does not exist
            if (extension_file_dict.get(extension) != None):                   # checks if there is an existing key value entry in dictionary
                extension_file_dict[extension].append(file_name)               # gets the list of files of that particular extension type and adds it
            else:
                extension_file_dict.update({extension : [file_name]})          # makes a new key value pair and adds it to dict

# checks validity of path, -1 = error, 0 = passed check
def check_path_validity():
    if (not os.path.exists(variables.FINAL_PATH)):
        showinfo(title="Target Folder Not Found", message="Target Folder Not Found.", detail="A new target folder will be made.") 
        try:
            os.mkdir(variables.FINAL_PATH)
            return 0
        except IOError as error:
            showerror(title="Target Folder", message="Target Folder Could Not Be Made", detail=error)
            print(f"{variables.ERROR_CODE}[ERROR]\tCould not make target folder : {error}{variables.END_CODE}")
            return -1
    return 0

# rename files of specific extension
def rename_spec_ext():
    # TODO: TRY TO IMPROVE, DO NOT BREAK
    user_want_to_continue_processing = False
    if (not extension_file_dict):
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        for extension, value_list in extension_file_dict.items():                                          # loop through list, giving extension, value of extension in dict
            randomized_list = value_list.copy()                                                             # copy into randomized list
            random.shuffle(randomized_list)                                                                 # shuffles

            for index, file_name in enumerate(value_list):                                                  # goes through shuffled list
                try:
                    final_file_name = randomized_list[index].rsplit('/', 1)[1]                              # makes final file name

                    original_file_path = f"{variables.SOURCE_PATH}{file_name}{extension}"                             # makes original file path
                    renamed_file_path = f"{variables.FINAL_PATH}/{final_file_name}{extension}"                        # makes replaced file path

                    try:
                        os.rename(original_file_path, renamed_file_path)                                    # actual renaming action
                    except IOError as error:
                        print(f"{variables.ERROR_CODE}[ERROR]\tCould not rename : {error}{variables.END_CODE}")
                        if (not user_want_to_continue_processing):
                            showerror(title="Error Linking", message=error)
                            user_want_to_continue_processing = askyesno(title="Do you want to continue", message="Do you still want to ignore this error and continue processing? This can lead to unexpected results")

                    log_text = f"Renaming {original_file_path}\nTO\n{renamed_file_path}\n"                  # Logging text parser
                    print(log_text)

                    if (variables.LOG):                                                                               # checks if log making is on
                        is_first_time = False                                                               # inits new first time var
                        if (index == 0):                                                                    # sees if first time log
                            is_first_time = True
                        log_file(is_first_time, log_text)

                except Exception as error:
                    showerror(title="Error Replacing", message="Files could not be replaced")
                    print(f"{variables.ERROR_CODE}[ERROR]\tCould not perform task : {error}{variables.END_CODE}")
        showinfo(title="Successful", message="Files were successfully randomized", detail="I wish you my randomized wishes for playing the game.")
        app.reset_variables()                                                                                   # Resets all variables for next replacement

# sets hard links from original image
def set_hard_links():

    total_elements_size = 0
    temp_file_path = "./tempfiles"
    user_want_to_continue = False

    # makes image pool with path : number of links
    image_link_map = {}
    for element in variables.IMG_DUPE_ARRAY:
        image_link_map.update({element: {
            "dupes": [],
            "current_hard_link": 1,
            "current_dupe_file_index": 0
        }})

    extension_img_dupe_file = ""

    if (not extension_file_dict):
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:

    # what it should do is
    # choose a random file
    # check if number of hard links is equal to limit
        # if yes, make temp file, append "dupes" array of map with that file and set hard link of that current file to 1
        # if no, continue
    # make a hard link
    # append the hard link counter in the map

        for extension, value_list in extension_file_dict.items():  # loop through list, giving extension, value of extension in dict
            for index, file_name in enumerate(value_list):          # goes through shuffled list
                try:
                    # choose a random file from the map
                    img_dupe_current_path, hard_link_current_limit = random.choice(list(image_link_map.items()))

                    if (hard_link_current_limit['current_hard_link'] == variables.HARD_LINK_LIMIT):
                        # make a temp file
                        try:
                            if (os.path.exists(temp_file_path)):
                                file_temp_name = img_dupe_current_path.rsplit('/', 1)[1]
                                temp_file = shutil.copy(img_dupe_current_path, f"{temp_file_path}/{hard_link_current_limit['current_dupe_file_index']}_{file_temp_name}")
                                hard_link_current_limit['dupes'].append(temp_file)

                                image_link_map.update({img_dupe_current_path: {
                                    "dupes": hard_link_current_limit['dupes'],
                                    "current_hard_link": 1,
                                    "current_dupe_file_index": hard_link_current_limit['current_dupe_file_index'] + 1
                                }})
                            else:
                                try:
                                    os.mkdir(temp_file_path)
                                except IOError as error:
                                    print(f"{variables.ERROR_CODE}[ERROR]\tCould not make temproary folder : {error}{variables.END_CODE}")
                        except IOError as error:
                            print(f"{variables.ERROR_CODE}[ERROR]\tCould not make temproary folder : {error}{variables.END_CODE}")
                    else:
                        temp_file = img_dupe_current_path

                    extension_img_dupe_file = temp_file.rsplit('.', 1)[1]
                
                    final_file_name = value_list[index].rsplit('/', 1)[1]                                   # makes final file name
                    renamed_file_path = f"{variables.FINAL_PATH}/{final_file_name}.{extension_img_dupe_file}"         # makes replaced file path

                    try:
                        os.link(temp_file, renamed_file_path)
                    except IOError as error:
                        print(f"{variables.ERROR_CODE}[ERROR]\tCould not make hard link : {error}{variables.END_CODE}")
                        if (not user_want_to_continue):
                            showerror(title="Error Linking", message=error)
                            user_want_to_continue = askyesno(title="Do you want to continue", message="Do you still want to ignore this error and continue processing? This can lead to unexpected results")

                    log_text = f"Hard Link from {temp_file}\nTO\n{renamed_file_path}\n"                      # Logging text parser
                    print(log_text)

                    try:
                        if (variables.LOG):                                                                           # checks if log making is on
                            is_first_time = False                                                           # inits new first time var
                            if (index == 0):                                                                # sees if first time log
                                is_first_time = True
                            log_file(is_first_time, log_text)
                    except Exception as error:
                        print(f"{variables.WARNING_CODE}[WARNING]\tLogging issue occured : {error}{variables.END_CODE}")
                    
                    hard_link_current_limit['current_hard_link'] += 1
                except Exception as error:
                    showerror(title="Error Replacing", message="Files could not be replaced")
                    print(f"{variables.ERROR_CODE}[ERROR]\tCould not perform task : {error}{variables.END_CODE}")

            # all things done
            try:
                os.remove(temp_file_path)
            except Exception as error:
                print(f"{variables.ERROR_CODE}[ERROR]\tCould not delete temp folder : {error}{variables.END_CODE}")

            showinfo(title="Successful", message="Files were successfully linked", detail="I wish you my randomized wishes for playing the game.")
            app.reset_variables()                                                               # Resets all variables for next replacement

# just makes config file by dumping json to a .json file
def make_config_file():

    app.set_variables()
    
    data={
        "source_path" : variables.SOURCE_PATH,
        "final_path": variables.FINAL_PATH,
        "seed": variables.SEED,
        "make_log_file": variables.LOG,
        "make_seeds_file": variables.SEED_SAVE,
        "filter_file_path": variables.FILTER_PATH,
        "show_tutorial": app.show_tutorial_bool.get()
    }

    try:   
        with open(variables.CONFIG_PATH, 'w') as config_file:
            json.dump(data, config_file)
        showinfo(title="Config Saved", message="Config File Has Been Saved")
    except FileNotFoundError as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tThe file 'config.json' was not found. {error}{variables.END_CODE}")
    except json.JSONDecodeError as error:
        print(f"{variables.WARNING_CODE}[ERROR]\tFailed to decode JSON from the file. {error}{variables.END_CODE}")

# reads config file, returns either json data, or empty
def read_config_file():
    try:   
        with open(variables.CONFIG_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError as error:
        print(f"{variables.WARNING_CODE}[WARNING]\tThe file 'config.json' was not found. {error}{variables.END_CODE}")
        return {}
    except json.JSONDecodeError as error:
        print(f"{variables.WARNING_CODE}[WARNING]\tFailed to decode JSON from the file. {error}{variables.END_CODE}")
        return {}

# This is to set the variables from config file, may throw error if config file is tampered with
def set_config_variables(config_data : dict):
    try:
        app.source_text.set(config_data["source_path"])
        app.target_text.set(config_data["final_path"])
        app.seed_text.set(config_data["seed"])
        app.make_log_bool.set(config_data["make_log_file"])
        app.filter_var.set(config_data["filter_file_path"])
        app.make_seed_bool.set(config_data["make_seeds_file"])
        app.show_tutorial_bool.set(config_data["show_tutorial"])
    except Exception as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tFailed to set configuration variables from config.json : {error}{variables.END_CODE}")
        showerror(title="Config Error", message="Config File Could Not Be Loaded")
        if(askyesno(title="Delete config.json?", message="Do you want to delete the corrupted config file?")):
            app.delete_files(variables.CONFIG_PATH)

# crypto miner, jk, this just notes the seeds in the seeds.txt file with timestamps
def seed_txt(seed : str):
    try:   
        with open(variables.SEED_SAVE_PATH, 'a') as seeds_file:
            seeds_file.write(f"{variables.TIMESTAMP} -> {seed}\n")
    except FileNotFoundError as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tThe file 'seeds.json' was not found. : {error}{variables.END_CODE}")

# Logging function, makes log.log file, accepts first_time, which sees if it is first time making log this session, and string_file, data for log
def log_file(first_time : bool, string_file : str):
    try:   
        with open(variables.LOG_PATH, 'a') as log_file:
            if (first_time):
                log_file.write(f"\n------{variables.TIMESTAMP}------\n\n")
            log_file.write(f"{string_file}\n")
    except FileNotFoundError as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tThe file 'log.log' was not found. : {error}{variables.END_CODE}")