'''
XP's Texture Randomizer Script
'''

# importing all requirementrs, does not require pip
import os
import random
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
import webbrowser
import json
import subprocess
import shutil

# core variables
# DO NOT CHANGE ON YOUR OWN
TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)    # generates a timestamp of when script is run
SEED = ""                                                   # PUT YOUR SEED HERE, wait that sounds wrong, i mean PUT THE SEED FOR THE RANDOMIZER HERE
SOURCE_PATH = "./textures/"                                 # This is the path for source textures
FINAL_PATH = "./replacements/"                              # this is the path where all textures will be moved
LOG = False                                                 # set True or False if you want log.log file generated
SEED_SAVE = False                                           # set True or False if you want seeds.txt generated
FILTER_PATH = "./filter.txt"                                # This is the path for filter
IMG_DUPE_PATH = ""                                          # This is the path for img dupe
IMG_DUPE_ARRAY = []                                         # This is the array for img dupe paths, key = img_path, value = number of times it is being used
ING_DUPE_BOOL = False                                       # This is the bool for img dupe
HARD_LINK_LIMIT = 1000                                      # Limit for hard links per file

# variables for tkinter styling
DEFAULT_FONT = ("Helvetica", 12)
DEFAULT_FONT_LABEL = ("Helvetica", 12, "bold")
DEFAULT_FONT_LABEL_SUBTITLE = ("Helvetica", 14, "bold")
DEFAULT_PADDING_X = 10
DEFAULT_PADDING_X_SUBTITLE = 20
DEFAULT_PADDING_Y = 5
DEFAULT_STICKY = "EW" 

file_list = []                                              # empty dict initialised before
# ---

extension_file_array = {}                                   # empty dict initialised before

# ------------------------------------------------------------
#                       CORE FUNCTION
# ------------------------------------------------------------

# this function does exactly that
def get_file_list():

    # This is the variable that stores the temproary data for the file names in the filter.txt file
    # This should contain data like `91fea45880122683-9788124e782590b3-00005994`, it should remove extensions from the names
    filter_file_list = []

    try:
        with open("./filter.txt", 'r') as filter_file:             
            for line in filter_file:                                                # parses lines from filter.txt to the array
                line.strip()                                                        # removes newline character
                if (line.find(".") != -1):
                    filter_file_list.append(line.rsplit('.', 1)[0])                 # removes the extension
    except:
        showwarning(title="Filter List", message="Filter List Not Found", detail="Filter List was not found or does not exist.")

    for file in file_list:                                                      # for loop to loop through files
        try:
            file_name, extension = os.path.splitext(file)                       # splits filename and extension
        except:
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
            if (extension_file_array.get(extension) != None):                   # checks if there is an existing key value entry in dictionary
                extension_file_array[extension].append(file_name)               # gets the list of files of that particular extension type and adds it
            else:
                extension_file_array.update({extension : [file_name]})          # makes a new key value pair and adds it to dict

# checks validity of path, -1 = error, 0 = passed check
def check_path_validity():
    if (not os.path.exists(SOURCE_PATH)):
        return -1
    
    if (not os.path.exists(FINAL_PATH)):
        showinfo(title="Target Folder Not Found", message="Target Folder Not Found.", detail="A new target folder will be made.") 
        try:
            os.mkdir(FINAL_PATH)
            return 0
        except IOError as error:
            showerror(title="Target Folder", message="Target Folder Could Not Be Made", detail=error)
            return -1
        
    return 0

# rename files of specific extension
def rename_spec_ext():
    # TODO: TRY TO IMPROVE, DO NOT BREAK
    user_want_to_continue = False
    if (not extension_file_array):
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        for extension, value_list in extension_file_array.items():                                          # loop through list, giving extension, value of extension in dict
            randomized_list = value_list.copy()                                                             # copy into randomized list
            random.shuffle(randomized_list)                                                                 # shuffles

            for index, file_name in enumerate(value_list):                                                  # goes through shuffled list
                try:
                    final_file_name = randomized_list[index].rsplit('/', 1)[1]                              # makes final file name

                    original_file_path = f"{SOURCE_PATH}{file_name}{extension}"                             # makes original file path
                    renamed_file_path = f"{FINAL_PATH}/{final_file_name}{extension}"                        # makes replaced file path

                    try:
                        os.rename(original_file_path, renamed_file_path)                                    # actual renaming action
                    except IOError as error:
                        print(error)
                        if (not user_want_to_continue):
                            showerror(title="Error Linking", message=error)
                            user_want_to_continue = askyesno(title="Do you want to continue", message="Do you still want to ignore this error and continue processing? This can lead to unexpected results")

                    log_text = f"Renaming {original_file_path}\nTO\n{renamed_file_path}\n"                  # Logging text parser
                    print(log_text)

                    if (LOG):                                                                               # checks if log making is on
                        is_first_time = False                                                               # inits new first time var
                        if (index == 0):                                                                    # sees if first time log
                            is_first_time = True
                        log_file(is_first_time, log_text)

                except:
                    showerror(title="Error Replacing", message="Files could not be replaced")
        showinfo(title="Successful", message="Files were successfully randomized")                          # Confirms all is done
        reset_variables()                                                                                   # Resets all variables for next replacement

# sets hard links from original image
def set_hard_links():

    total_elements_size = 0
    temp_file_path = "./tempfiles"
    user_want_to_continue = False

    # makes image pool with path : number of links
    image_link_map = {}
    for element in IMG_DUPE_ARRAY:
        image_link_map.update({element: {
            "dupes": [],
            "current_hard_link": 1,
            "current_dupe_file_index": 0
        }})             # element - path of image

    temp_file_array = []
    extension_img_dupe_file = ""

    if (not extension_file_array):
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        for values in extension_file_array.values():  # loop through list, giving extension, value of extension in dict
            total_elements_size = total_elements_size + len(values)

    # what it should do is
    # choose a random file
    # check if number of hard links is equal to limit
        # if yes, make temp file, replace key of map with that file and value of that file back to 1
        # if no, continue
    # make a hard link
    # append the hard link counter in the map

    for extension, value_list in extension_file_array.items():  # loop through list, giving extension, value of extension in dict
        for index, file_name in enumerate(value_list):          # goes through shuffled list
            try:
                # choose a random file from the map

                img_dupe_current_path, hard_link_current_limit = random.choice(list(image_link_map.items()))

                if (hard_link_current_limit['current_hard_link'] == HARD_LINK_LIMIT):
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
                                print("Couldn't make folder : " + error)

                        print(image_link_map[img_dupe_current_path])
                    except IOError as error:
                        print("failed to make temp folder")
                        print(error)
                else:
                    temp_file = img_dupe_current_path

                extension_img_dupe_file = temp_file.rsplit('.', 1)[1]
            
                final_file_name = value_list[index].rsplit('/', 1)[1]                                   # makes final file name
                renamed_file_path = f"{FINAL_PATH}/{final_file_name}.{extension_img_dupe_file}"         # makes replaced file path

                try:
                    os.link(temp_file, renamed_file_path)
                except IOError as error:
                    print(error)
                    if (not user_want_to_continue):
                        showerror(title="Error Linking", message=error)
                        user_want_to_continue = askyesno(title="Do you want to continue", message="Do you still want to ignore this error and continue processing? This can lead to unexpected results")

                log_text = f"Hard Link from {temp_file}\nTO\n{renamed_file_path}\n"                      # Logging text parser
                print(log_text)

                try:
                    if (LOG):                                                                           # checks if log making is on
                        is_first_time = False                                                           # inits new first time var
                        if (index == 0):                                                                # sees if first time log
                            is_first_time = True
                        log_file(is_first_time, log_text)
                except:
                    print("Logging Issue Occured")
                
                hard_link_current_limit['current_hard_link'] += 1
            except:
                showerror(title="Error Replacing", message="Files could not be replaced")

        # all things done
        try:
            os.remove(temp_file_path)
        except:
            print("could not remove temp files")

        showinfo(title="Successful", message="Files were successfully linked")          # Confirms all is done
        reset_variables()                                                               # Resets all variables for next replacement

# just makes config file by dumping json to a .json file
def make_config_file():

    set_variables()
    
    data={
        "source_path" : SOURCE_PATH,
        "final_path": FINAL_PATH,
        "seed": SEED,
        "make_log_file": LOG,
        "make_seeds_file": SEED_SAVE,
        "filter_file_path": FILTER_PATH,
    }

    try:   
        with open("./config.json", 'w') as config_file:
            json.dump(data, config_file)
        showinfo(title="Config Saved", message="Config File Has Been Saved")
    except FileNotFoundError:
        print("Error: The file 'config.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")

# reads config file, returns either json data, or empty
def read_config_file():
    try:   
        with open("./config.json", 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Error: The file 'config.json' was not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")
        return {}

# This is to set the variables from config file, may throw error if config file is tampered with
def set_config_variables(config_data : dict):
    try:
        source_text.set(config_data["source_path"])
        target_text.set(config_data["final_path"])
        seed_text.set(config_data["seed"])
        make_log_bool.set(config_data["make_log_file"])
        filter_var.set(config_data["filter_file_path"])
        make_seed_bool.set(config_data["make_seeds_file"])
    except:
        # TODO : Make a delete function for corrupt config file
        showerror(title="Config Error", message="Config File Could Not Be Loaded")

# crypto miner, jk, this just notes the seeds in the seeds.txt file with timestamps
def seed_txt(seed : str):
    try:   
        with open("./seeds.txt", 'a') as seeds_file:
            seeds_file.write(f"{TIMESTAMP} -> {seed}\n")
    except FileNotFoundError:
        print("Error: The file 'seeds.json' was not found.")

# Logging function, makes log.log file, accepts first_time, which sees if it is first time making log this session, and string_file, data for log
def log_file(first_time : bool, string_file : str):
    try:   
        with open("./log.log", 'a') as log_file:
            if (first_time):
                log_file.write(f"\n------{TIMESTAMP}------\n\n")
            log_file.write(f"{string_file}\n")
    except FileNotFoundError:
        print("Error: The file 'log.log' was not found.")

# It resets variables after replacement of all textures is done
def reset_variables():
    global file_list
    try:
        source_text.set("")
        target_text.set("")
        seed_text.set("")
        img_dupe_use_var.set(False)
        img_dupe_var.set("")
        file_list = []
    except:
        print("Error resetting vars")

# ------------------------------------------------------------
#                   TKINTER CORE FUNCTIONS
# ------------------------------------------------------------

# opens my github tutorial readme.md
def open_github_button_action():
    webbrowser.open("https://gist.github.com/real-xp/e9f5b9bb9f416043a9f7dc6e9ab3a7f6#file-readme-md")

    # Folder Picker dialog box for both Source And Target Folders

# dialog box action for folders, and 
def dialog_box_button_action(action : str, type_of_action : str):
    global FILTER_PATH, IMG_DUPE_PATH
    if (type_of_action == "FOLDER"):
        dialog_path = filedialog.askdirectory(title=f"Choose {action} Path", initialdir="./")
    else:
        dialog_path = filedialog.askopenfilename(title=f"Choose {action} Path", initialdir="./", filetypes=[("Text File", "*.txt")])
    if (dialog_path != ""):
        if (action == "Source"):
            source_text.set(dialog_path)
        elif (action == "Target"):
            target_text.set(dialog_path)
        elif (action == "Filter"):
            FILTER_PATH = dialog_path
            filter_var.set(FILTER_PATH)

# select image pool function
def dialog_box_multi_select_img_dupe():
    global IMG_DUPE_ARRAY
    dialog_path_array = filedialog.askopenfilenames(title=f"Choose Images", initialdir="./", filetypes=[("PNG", "*.png"), ("DDS", "*.dds"), ("BMP", "*.bmp"), ("All Files", "*")])
    if (dialog_path_array != []):
        IMG_DUPE_ARRAY = dialog_path_array
        img_dupe_input['values'] = IMG_DUPE_ARRAY
            
# Opens Notepad When Button Pressed
def open_notepad_window(type_of_action):
    # TODO : REMOVE HARDCODED PATHS
    if (type_of_action == "LOG"):
        subprocess.run(["notepad","./log.log"])
    elif (type_of_action == "SEED"):
        subprocess.run(["notepad","./seeds.txt"])
    elif (type_of_action == "FILTER"):
        subprocess.run(["notepad","./filter.txt"])
    else:
        showerror(title="Error", message="Some Kind Of Error Occured")

# deletes file of log and seed
def delete_files(type_of_action):
    # TODO : REMOVE HARDCODED PATHS
    try:
        if (type_of_action == "LOG"):
            os.remove("./log.log")
        elif (type_of_action == "SEED"):
            os.remove("./seeds.txt")
        elif (type_of_action == "CONFIG"):
            os.remove("./config.json")
        else:
            showerror(title="Error", message="Some kind of error occured while deleting.")
        showinfo(title="Successful", message="File was successfully deleted.")
    except OSError:
        showerror(title="Error", message="Some kind of error occured while deleting.")

        # set variables for use

# randomise button pressed, does checks        
def pressed_ranomise_button():
    # Multiple Checks
    if (source_text.get() == ""):                               # sees if source entry is empty
        showerror(title="Error",message="Source Path Empty" , detail="Source path is empty. Please fill in the path.")
        return
    
    if (img_dupe_use_var.get()):
        message = "Are you sure you want to continue? This will link the image you chose to multiple files with names from SOURCE folder and put them in TARGET folder"

        if (IMG_DUPE_ARRAY == []):                              # sees if img_dupe entry is empty
            showerror(title="Error",message="Image Dupe List Empty" , detail="Image Dupe list is empty. Please choose some image files.")
            return
    else:
        message = "Are you sure you want to continue? This WILL rename EVERY and ALL files in the SOURCE folder, regardless if they are images or not and move them to the TARGET folder."

    if (target_text.get() == ""):                               # sees if target entry is empty
            showerror(title="Error",message="Target Path Empty" , detail="Target path is empty. Please fill in the path.")
            return
    
    if (target_text.get() == source_text.get()):                # sees if both are same path
            showerror(title="Error",message="Source and Target Paths Conflict" , detail="Source and Target Paths cannot be same.")
            return

    last_confirmation = askyesno(title="Are you sure?", message=message)
    if (last_confirmation):                                     # asks user one last time if they want to continue
        main_randomizer_task(img_dupe_use_var.get())

# sets variables
def set_variables():
    global SOURCE_PATH, FINAL_PATH, SEED, LOG, SEED_SAVE, FILTER_PATH, IMG_DUPE_PATH, ING_DUPE_BOOL
    SOURCE_PATH = source_text.get()
    FINAL_PATH = target_text.get()
    SEED = seed_text.get()
    LOG = make_log_bool.get()
    SEED_SAVE = make_seed_bool.get()
    FILTER_PATH = filter_var.get()
    IMG_DUPE_PATH = img_dupe_var.get()
    ING_DUPE_BOOL = img_dupe_use_var.get()

    # main randomizer body

# main place where randomisation initially passes checks
def main_randomizer_task(is_image_duping_action : bool):
    # Set variable values
    global SOURCE_PATH, FINAL_PATH, SEED, FILTER_PATH, file_list
    set_variables()

    # removing \ to use / in path, if user didnt use choose button
    SOURCE_PATH = SOURCE_PATH.replace("\\", "/")
    FINAL_PATH = FINAL_PATH.replace("\\", "/")

    # testing if filelist can even be detected
    try:
        for root, dirs, files in os.walk(SOURCE_PATH):              # parses and recursively gets all files in text
            for n in files:
                fp = os.path.join(root, n)
                ft = fp.replace(SOURCE_PATH, "")
                fl = ft.replace("\\", "/")
                file_list.append(fl)
    except:
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
        file_list = []

    # sees if file list is not empty
    if (file_list != []):
        if (FILTER_PATH == ""):                                     # checks if filter path is not empty
            FILTER_PATH = "./filter.txt"                            # puts default path link as safety check

        if (SEED == ''):                                            # checks if user left seed input field empty
            SEED = str(random.randint(0, pow(2, 32)))               # chooses random int between 0 and 2**32

        random.seed(SEED)                                           # sets the seed into random pkg

        if (SEED_SAVE):                                             # checks if seed saving is turned on
            seed_txt(SEED)                                          # puts the seed into seed history file

        if (check_path_validity() == 0):                            # checks if path is valid
            get_file_list()                                         # calls on file filter and file collector
            if (not is_image_duping_action):
                rename_spec_ext()                                   # actual renaming function
            else:
                if (not askyesno(title="Are You SURE?", message="This method invloves making Hard Links from the image file you provided and make thousands of linked files. This approach uses less storage than copying, but has a lot of limitations. Do you still want to continue?")):
                    return
                if (not askyesno(title="Are You REALLY SURE?", message="As windows puts a limit of 1024 hard links including original image file, this program will create multiple temproary files in case of thousands of files. There are more limitations. Do you want to still continue?")):
                    return
                if (not askyesno(title="Are You REALLY REALLY SURE?", message="Hard Links are also not possible on a USB Stick or a partition of a drive formatted with FAT32. This means if your drive is FAT32, please do not continue. Do you still wish to continue")):
                    return
                if (not askyesno(title="Are You REALLY REALLY REALLY SURE?", message="If you have done this process before, and deleted the linked files, but they are still in recycling bin, PLEASE DELETE THOSE FILES AS THEY STILL COUNT AS HARD LINKS AND COUNT TOWARDS THE ORIGINAL IMAGE LIMIT. IF YOU DONT DELETE, THE PROGRAM WILL CRASH AND WILL NOT GENERATE IMAGES. Do you still wish to continue?")):
                    return
                set_hard_links()
        else:
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")

# change text to dump or randomize
def change_text_to_dupe():
    if (img_dupe_use_var.get()):
        target_button.config(text="DUPLICATE TEXTURES")
    else:
        target_button.config(text="RANDOMIZE TEXTURES")

# revert combo box completely
def revert_combo_box(event=""):
    img_dupe_var.set("Click here to see all images in pool")

# ------------------------------------------------------------
#                   TKINTER WINDOW SETTINGS
# ------------------------------------------------------------

# opens settings window
def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("600x440")
    settings_window.resizable(False,False)

    # defining column weight
    settings_window.columnconfigure(index=0, weight=5)

    # Top Bar
    title_label = ttk.Label(settings_window, text="Settings", font=("Helvetica", 22, "bold"))

    # Seeds section
    seed_title = ttk.Label(settings_window, text="Seeds", style="Subtitle.TLabel")
    seed_save_checkbox = ttk.Checkbutton(settings_window, text="Make Seed History", variable=make_seed_bool)
    seed_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window("SEED"))
    seed_file_delete = ttk.Button(settings_window, text="Delete", command=lambda:delete_files("SEED"))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=5, padx=DEFAULT_PADDING_X ,pady=(5,0), sticky=DEFAULT_STICKY)

    # Logs section
    logs_title = ttk.Label(settings_window, text="Logs", style="Subtitle.TLabel")
    logs_save_checkbox = ttk.Checkbutton(settings_window, text="Make Logs", variable=make_log_bool)
    logs_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window("LOG"))
    logs_file_delete = ttk.Button(settings_window, text="Delete", command=lambda:delete_files("LOG"))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=5, padx=DEFAULT_PADDING_X ,pady=(5,0), sticky=DEFAULT_STICKY)

    # Filter section
    filter_title = ttk.Label(settings_window, text="Filter", style="Subtitle.TLabel")
    filter_file_title = ttk.Entry(settings_window, state="disabled", textvariable=filter_var)
    filter_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window("FILTER"))
    filter_file_choose = ttk.Button(settings_window, text="Choose", command=lambda: dialog_box_button_action(action="Filter", type_of_action="FILE"))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=5, padx=DEFAULT_PADDING_X ,pady=(5,0), sticky=DEFAULT_STICKY)

    # Filter section
    tutorial_title = ttk.Label(settings_window, text="Tutorial", style="Subtitle.TLabel")
    tutorial_file_title = ttk.Label(settings_window, text="To read tutorial, click here ->")
    tutorial_file_open = ttk.Button(settings_window, text="Open GitHub", command=open_github_button_action)

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=12, column=0, columnspan=5, padx=DEFAULT_PADDING_X ,pady=(5,0), sticky=DEFAULT_STICKY)

    # Config section

    about_me = ttk.Label(settings_window, text="Made by realXP (XP)")

    config_file_clear = ttk.Button(settings_window, text="Clear Settings", command=lambda: delete_files("CONFIG"))
    config_file_save = ttk.Button(settings_window, text="Save Settings", command=make_config_file)

    # Placing Elements

    # Top Bar
    title_label.grid(row=0, column=0, columnspan=2, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_X, sticky='EW')

    # Seeds Section
    seed_title.grid(row=1, column=0, padx=DEFAULT_PADDING_X_SUBTITLE, pady=0, sticky='w')
    seed_save_checkbox.grid(row=2, column=0, columnspan=2, padx=DEFAULT_PADDING_X_SUBTITLE, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    seed_file_open.grid(row=2, column=2, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    seed_file_delete.grid(row=2, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
   
    # Log Section
    logs_title.grid(row=4, column=0, padx=DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    logs_save_checkbox.grid(row=5, column=0, columnspan=2, padx=DEFAULT_PADDING_X_SUBTITLE, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    logs_file_open.grid(row=5, column=2, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    logs_file_delete.grid(row=5, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    # Filter Section
    filter_title.grid(row=7, column=0, padx=DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    filter_file_title.grid(row=8, column=0, columnspan=2, padx=DEFAULT_PADDING_X_SUBTITLE, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    filter_file_open.grid(row=8, column=2, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    filter_file_choose.grid(row=8, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    # Tutorial Section
    tutorial_title.grid(row=10, column=0, padx=DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    tutorial_file_title.grid(row=11, column=0, columnspan=3, padx=DEFAULT_PADDING_X_SUBTITLE, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    tutorial_file_open.grid(row=11, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    # Config Section
    about_me.grid(row=13, column=0, columnspan=2, padx=DEFAULT_PADDING_X_SUBTITLE, pady=DEFAULT_PADDING_X_SUBTITLE, sticky=DEFAULT_STICKY)
    config_file_clear.grid(row=13, column=2, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_X_SUBTITLE, sticky=DEFAULT_STICKY)
    config_file_save.grid(row=13, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_X_SUBTITLE, sticky=DEFAULT_STICKY)

# ------------------------------------------------------------
#                   TKINTER WINDOW MAIN
# ------------------------------------------------------------

# main body of the program, this runs the tkinter window
def main():
    global root

    # defining root window
    root = tk.Tk()
    root.title("PCSX2 Texture Randomizer")
    root.geometry("900x360")
    root.resizable(False,False)

    # defining styles for ttk widgets
    root.style = ttk.Style(root)
    root.style.configure('TLabel', font=DEFAULT_FONT_LABEL)
    root.style.configure('TButton', font=DEFAULT_FONT_LABEL)
    root.style.configure('TCheckbutton', font=DEFAULT_FONT_LABEL)
    root.style.configure("Export.TButton", font = ("Helvetica", 16, "bold"))
    root.style.configure("Save.TButton", font=DEFAULT_FONT_LABEL)
    root.style.configure("Subtitle.TLabel", font=DEFAULT_FONT_LABEL_SUBTITLE)

    # defining column weight
    root.columnconfigure(index=1, weight=5)

    # VARIABLES
    global source_text, target_text, seed_text, make_log_bool, save_config_bool, progress_bar_var, make_seed_bool, filter_var, img_dupe_var, img_dupe_use_var

    source_text = tk.StringVar()                                # takes source string from input
    target_text = tk.StringVar()                                # takes target string from input
    seed_text = tk.StringVar()                                  # takes seed from input
    make_log_bool = tk.BooleanVar()                             # takes checkbox boolean value of log
    make_seed_bool = tk.BooleanVar()                            # takes checkbox boolean value of seed
    progress_bar_var = tk.StringVar()                           # stores progress bar data for update purposes
    filter_var = tk.StringVar()                                 # stores filter_file path
    img_dupe_var = tk.StringVar()                               # stores img_dupe path
    revert_combo_box()
    img_dupe_use_var = tk.BooleanVar()                          # takes checkbox boolean value of img_dupe

    config_data = read_config_file()                            # reads the config file
    if (config_data != {}):
        set_config_variables(config_data=config_data)           # if config file exists, set values to config file ones

    # Top Bar
    title_label = ttk.Label(root, text="PCSX2 Texture Randomizer", font=("Helvetica", 22, "bold"))
    about_button = ttk.Button(root, text="Settings", command=open_settings_window)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=(0, 20), sticky=DEFAULT_STICKY)

    # Mid level
    source_input_label = ttk.Label(root, text="Source Path")
    source_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=source_text)
    source_dialogue = ttk.Button(root, text="Choose", command=lambda: dialog_box_button_action(action="Source", type_of_action="FOLDER"))

    target_input_label = ttk.Label(root, text="Target Path")
    target_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=target_text)
    target_dialogue = ttk.Button(root, text="Choose", command=lambda: dialog_box_button_action(action="Target", type_of_action="FOLDER"))

    seed_input_label = ttk.Label(root, text="Seed")
    seed_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=seed_text)
    seed_validate = ttk.Button(root, text="Random", command=lambda: seed_text.set(str(random.randint(0, pow(2, 32)))))

    global img_dupe_input
    img_dupe_input_label = ttk.Label(root, text="Image Dupe")
    img_dupe_input = ttk.Combobox(root, textvariable=img_dupe_var, state="readonly", font=DEFAULT_FONT)
    img_dupe_input.bind("<<ComboboxSelected>>", revert_combo_box)
    img_dupe_use = ttk.Checkbutton(root, text="Use", variable=img_dupe_use_var, command=change_text_to_dupe)
    img_dupe_choose = ttk.Button(root, text="Choose", command=dialog_box_multi_select_img_dupe)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=5, pady=10, sticky=DEFAULT_STICKY)

    # Target Button
    global target_button
    target_button = ttk.Button(root, text="RANDOMIZE TEXTURES", style="Export.TButton", command=pressed_ranomise_button)

    # PLACING ALL ELEMENTS DOWN
   
   # Top Bar
    title_label.grid(row=0, column=0, columnspan=2, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_X, sticky='EW')
    about_button.grid(row=0, column=3, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_X_SUBTITLE, ipadx=10, ipady=10, sticky=DEFAULT_STICKY)
   
   # Mid Bar
    source_input_label.grid(row=2, column=0, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky='w')
    source_input.grid(row=2, column=1, columnspan=2, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    source_dialogue.grid(row=2, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    target_input_label.grid(row=3, column=0, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky='w')
    target_input.grid(row=3, column=1, columnspan=2, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    target_dialogue.grid(row=3, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    seed_input_label.grid(row=4, column=0, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky='w')
    seed_input.grid(row=4, column=1, columnspan=2, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    seed_validate.grid(row=4, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    img_dupe_input_label.grid(row=5, column=0, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky='w')
    img_dupe_input.grid(row=5, column=1, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    img_dupe_use.grid(row=5, column=2, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)
    img_dupe_choose.grid(row=5, column=3, columnspan=1, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, sticky=DEFAULT_STICKY)

    target_button.grid(row=7, column=0, columnspan=5, padx=DEFAULT_PADDING_X, pady=DEFAULT_PADDING_Y, ipadx=25, ipady=10, sticky=DEFAULT_STICKY)

    root.mainloop()

# This is to ensure the program is run as a separate file and not a package
if __name__ == "__main__":
    main()                                                  # calls on main function