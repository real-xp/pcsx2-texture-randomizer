'''
XP's Texture Randomiser Script
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

# core variables
# DO NOT CHANGE ON YOUR OWN
TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)    # generates a timestamp of when script is run
SEED = ""                                                   # PUT YOUR SEED HERE, wait that sounds wrong, i mean PUT THE SEED FOR THE RANDOMISER HERE
SOURCE_PATH = "./textures/"                                 # This is the path for source textures
FINAL_PATH = "./replacements/"                              # this is the path where all textures will be moved
LOG = False                                                 # set True or False if you want log.log file generated
CONFIG = False                                              # set True or False if you want config.json generated

# variables for tkinter styling
DEFAULT_FONT = ("Helvetica", 12)
DEFAULT_FONT_NOTEPAD = ("Helvetica", 11)
DEFAULT_FONT_LABEL = ("Helvetica", 12, "bold")
DEFAULT_PADDING = 10
DEFAULT_STICKY = "EW" 

file_list = []                                              # empty dict initialised before
# ---

extension_file_array = {}                                   # empty dict initialised before

# ------------------------------------------------------------
#                       CORE FUNCTION
# ------------------------------------------------------------

# this function does exactly that
def get_file_list():
    # filter files

    # initialises an empty filter list
    filter_file_list = []

    try:
        with open("./filter.txt", 'r') as filter_file:
            # filter_file_list = [line.strip() for line in filter_file]               
            for line in filter_file:                                                # parses lines from filter.txt to the array
                line.strip()                                                        # removes newline character
                if (line.find(".") != -1):
                    filter_file_list.append(line.rsplit('.', 1)[0])                 # removes the extension
    except:
        showwarning(title="Filter List", message="Filter List Not Found", detail="Filter List was not found or does not exist.")

    for file in file_list:                                                          # for loop to loop through files
        try:
            file_name, extension = os.path.splitext(file)                           # splits filename and extension

            file_is_in_filter = False                                               # filter bool

            for filter_element in filter_file_list:                                 # checks if filename is in filter
                if filter_element in file_name:
                    file_is_in_filter = True
                    break

            if (not file_is_in_filter):                                             # checks if file is in filter list
                if (extension != ''):                                               # checks if somehow extension does not exist
                    if (extension_file_array.get(extension) != None):               # checks if there is an existing key value entry in dictionary
                        temp_list_array = extension_file_array[extension]           # gets the list of files of that particular extension type
                        temp_list_array.append(file_name)                           # adds current iteration file name into that list
                    else:
                        extension_file_array.update({extension : [file_name]})      # makes a new key value pair and adds it to dict
        except:
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
            continue

# checks validity of path, -1 = error, 0 = passed check
def check_path_validity():
    if (os.path.exists(SOURCE_PATH)):
        if (os.path.exists(FINAL_PATH)):
            return 0
        else:
            showinfo(title="Target Folder", message="Target Folder Not Found", detail="A new target folder will be made.")
            try:
                os.mkdir(FINAL_PATH)
                return 0
            except:
                showerror(title="Target Folder", message="Target Folder Could Not Be Made")
                return -1
    else:
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
        return -1

# rename files of specific extension
def rename_spec_ext():

    value_list_size = 0

    if (not extension_file_array):
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        progress_log_window()
        for extension, value_list in extension_file_array.items():  # loop through list, giving extension, value of extension in dict
            randomised_list = value_list.copy()                     # copy into randomised list
            random.shuffle(randomised_list)                         # shuffles
            value_list_size = len(value_list)

            for index, file_name in enumerate(value_list):          # goes through shuffled list
                try:
                    final_file_name = randomised_list[index].rsplit('/', 1)[1]                              # makes final file name

                    original_file_path = f"{SOURCE_PATH}{file_name}{extension}"                             # makes original file path
                    renamed_file_path = f"{FINAL_PATH}/{final_file_name}{extension}"                        # makes replaced file path

                    try:
                        log_text = f"Renaming {original_file_path}\nTO\n{renamed_file_path}"                # Logging text parser
                        log_text_label.config(state="normal")                                               # sets state to normal so the logging window is user editable
                        log_text_label.insert(tk.END, f"{log_text}\n\n")

                        # progress bar
                        current_progress = (index / value_list_size)                                        # for progress bar percentage
                        progress_bar['value'] = current_progress                                            # sets progress bar value
                        progress_bar_var.set(f"{current_progress*100}% - {index+1} / {value_list_size}")    # progress text value
                    except:
                        print("Log window closed")

                    if (LOG):                                               # checks if log making is on
                        is_first_time = False                               # inits new first time var
                        if (index == 0):                                    # sees if first time log
                            is_first_time = True
                        log_file(is_first_time, log_text)
                    os.rename(original_file_path, renamed_file_path)        # actual renaming action
                except:
                    showerror(title="Error Replacing", message="Files could not be replaced")

        # all things done
        log_text_label.config(state="disabled")                                         # sets status of log window diabled so user cant edit
        progress_bar['value'] = 100                                                     # progress set to 100
        progress_bar_var.set(f"100% - {value_list_size} / {value_list_size}")           # progress text set to max
        showinfo(title="Successful", message="Files were successfully randomised")      # Confirms all is done
        reset_variables()                                                               # Resets all variables for next replacement

# just makes config file by dumping json to a .json file
def make_config_file(data):
    try:   
        with open("./config.json", 'w') as config_file:
            json.dump(data, config_file)
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
def set_config_variables(config_data):
    global SOURCE_PATH, FINAL_PATH, SEED, LOG, CONFIG
    try:
        SOURCE_PATH = source_text.set(config_data["source_path"])
        FINAL_PATH = target_text.set(config_data["final_path"])
        SEED = seed_text.set(config_data["seed"])
        LOG = make_log_bool.set(config_data["make_log_file"])
        CONFIG = save_config_bool.set(config_data["make_config_file"])
    except:
        # TODO : Make a delete function for corrupt config file
        showerror(title="Config Error", message="Config File Could Not Be Loaded")

# crypto miner, jk, this just notes the seeds in the seeds.txt file with timestamps
def seed_txt(seed):
    try:   
        with open("./seeds.txt", 'a') as seeds_file:
            seeds_file.write(f"{TIMESTAMP} -> {seed}\n")
    except FileNotFoundError:
        print("Error: The file 'seeds.json' was not found.")

# Logging function, makes log.log file, accepts first_time, which sees if it is first time making log this session, and string_file, data for log
def log_file(first_time, string_file):
    try:   
        with open("./log.log", 'a') as log_file:
            if (first_time):
                log_file.write(f"\n------{TIMESTAMP}------\n\n")
            log_file.write(f"{string_file}\n")
    except FileNotFoundError:
        print("Error: The file 'log.log' was not found.")

# It resets variables after replacement of all textures is done
def reset_variables():
    global SOURCE_PATH, FINAL_PATH, SEED, file_list
    try:
        SOURCE_PATH = source_text.set("")
        FINAL_PATH = target_text.set("")
        SEED = seed_text.set("")
        file_list = []
    except:
        print("Error resetting vars")

# ------------------------------------------------------------
#                       TKINTER WINDOW
# ------------------------------------------------------------

# Opens the log + progress bar window
def progress_log_window():
    global log_window

    # makes new window for logging
    log_window = tk.Toplevel(root)
    log_window.title("Executing")
    log_window.geometry("900x450")
    log_window.resizable(0,0)

    log_main_frame = tk.Frame(log_window)
    log_main_frame.pack(fill='both', expand=True)

    log_text_label_scroll = tk.Scrollbar(log_main_frame)
    log_text_label_scroll.pack(fill="y", side='right')

    global log_text_label, progress_bar

    # main logger
    log_text_label = tk.Text(log_main_frame, state="disabled")                  # initially disabled so user cannot edit anything
    log_text_label.pack(expand=True, fill="both", side='left')  

    # scrollbar behaviour
    log_text_label['yscrollcommand']=log_text_label_scroll.set
    log_text_label_scroll.config(command=log_text_label.yview)

    progress_bar = ttk.Progressbar(log_window, orient='horizontal', mode='determinate')
    progress_bar.pack(expand=True, fill='x', padx=5)
    progress_bar_label = ttk.Label(log_window, text="0%", textvariable=progress_bar_var)
    progress_bar_label.pack(expand=True, fill='x', padx=5)

# opens my github tutorial readme.md
def open_github_button_action():
    webbrowser.open("https://gist.github.com/real-xp/e9f5b9bb9f416043a9f7dc6e9ab3a7f6#file-readme-md")

# Folder Picker dialog box for both Source And Target Folders
def dialog_box_button_action(action):
    dialog_path = filedialog.askdirectory(title="Choose A {action} Path")
    if (dialog_path != ""):
        if (action == "Source"):
            source_text.set(dialog_path)
        elif (action == "Target"):
            target_text.set(dialog_path)

# Opens Notepad When Button Pressed
def note_tkinter_window(type_of_action):
    if (type_of_action == "LOG"):
        subprocess.run(["notepad","./log.log"])
    elif (type_of_action == "SEED"):
        subprocess.run(["notepad","./seeds.txt"])
    elif (type_of_action == "FILTER"):
        subprocess.run(["notepad","./filter.txt"])
    else:
        showerror(title="Error", message="Some Kind Of Error Occured")
        
def pressed_ranomise_button(config_data):
    # Multiple Checks
    if (source_text.get() == ""):                           # sees if source entry is empty
        showerror(title="Error",message="Source Path Empty" , detail="Source path is empty. Please fill in the path.")
        return

    if (target_text.get() == ""):                           # sees if target entry is empty
        showerror(title="Error",message="Target Path Empty" , detail="Target path is empty. Please fill in the path.")
        return
    
    if (target_text.get() == source_text.get()):            # sees if both are same path
        showerror(title="Error",message="Source and Target Paths Conflict" , detail="Source and Target Paths cannot be same.")
        return
    
    last_confirmation = askyesno(title="Are you sure?", message="Are you sure you want to continue? This WILL rename EVERY and ALL files in the SOURCE folder, regardless if they are images or not and move them to the TARGET Folder.")
    if (last_confirmation):                                 # asks user one last time if they want to continue
        main_randomiser_task(config_data)

# main randomiser body
def main_randomiser_task(config_data):
    # Set variable values
    global SOURCE_PATH, FINAL_PATH, SEED, LOG, CONFIG
    SOURCE_PATH = source_text.get()
    FINAL_PATH = target_text.get()
    SEED = seed_text.get()
    LOG = make_log_bool.get()
    CONFIG = save_config_bool.get()

    # testing if filelist can even be detected
    global file_list
    try:
        for root, dirs, files in os.walk(SOURCE_PATH):              # parses and recursively gets all files in text
            for n in files:
                fp = os.path.join(root, n)
                ft = fp.replace(SOURCE_PATH, "")
                fl = ft.replace("\\", "/")
                file_list.append(fl)
        # file_list = os.listdir(path=SOURCE_PATH) OLD NON RECURSIVE METHOD
    except:
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")

    # saving configuration
    if (CONFIG):
        config_data = {
            "source_path" : SOURCE_PATH,
            "final_path": FINAL_PATH,
            "seed": SEED,
            "make_log_file": LOG,
            "make_config_file": CONFIG,
        }
        make_config_file(config_data)                               # calls the config making function

    # sees if file list is not empty
    if (file_list != []):
        if (SEED != ''):                                            # checks if user left seed input field empty
            random.seed(SEED)                                       # set seed
            seed_txt(SEED)                                          # seed logger
        else:
            temp_rand_seed = str(random.randint(0, pow(2, 32)))     # chooses random int between 0 and 2**32
            random.seed(temp_rand_seed)
            seed_txt(temp_rand_seed)

        if (check_path_validity() == 0):                            # checks if path is valid
            get_file_list()                                         # calls on file filter and file collector
            rename_spec_ext()                                       # actual renaming function
        else:
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")

# main body of the program, this runs the tkinter window
def main():
    global root

    # defining root window
    root = tk.Tk()
    root.title("PCSX2 Texture Randomiser")
    root.geometry("900x450")
    root.resizable(0,0)

    # defining styles for ttk widgets
    root.style = ttk.Style(root)
    root.style.configure('TLabel', font=DEFAULT_FONT_LABEL)
    root.style.configure('TButton', font=DEFAULT_FONT_LABEL)
    root.style.configure('TCheckbutton', font=DEFAULT_FONT_LABEL)
    root.style.configure("Export.TButton", font = ("Helvetica", 16, "bold"))
    root.style.configure("Save.TButton", font=DEFAULT_FONT_LABEL)

    # defining column weight
    root.columnconfigure(index=1, weight=5)

    # importing icons for buttons
    # TODO: Remove this, add base64 function later
    github_icon = tk.PhotoImage(file='./assets/github.png')
    folder_icon = tk.PhotoImage(file='./assets/folder.png')
    random_icon = tk.PhotoImage(file='./assets/random.png')
    export_icon = tk.PhotoImage(file='./assets/export.png')


    # VARIABLES
    global source_text, target_text, seed_text, make_log_bool, save_config_bool, progress_bar_var

    source_text = tk.StringVar()                                # takes source string from input
    target_text = tk.StringVar()                                # takes target string from input
    seed_text = tk.StringVar()                                  # takes seed from input
    make_log_bool = tk.BooleanVar()                             # takes checkbox boolean value of log
    save_config_bool = tk.BooleanVar()                          # takes checkbox boolena value of config
    progress_bar_var = tk.StringVar()                           # stores progress bar data for update purposes

    config_data = read_config_file()                            # reads the config file
    if (config_data != {}):
        set_config_variables(config_data=config_data)           # if config file exists, set values to config file ones

    # Top Bar
    title_label = ttk.Label(root, text="PCSX2 Texture Randomiser", font=("Helvetica", 22, "bold"))
    about_button = ttk.Button(root, image=github_icon, command=open_github_button_action)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=(0, 20), sticky=DEFAULT_STICKY)

    # Mid level
    source_input_label = ttk.Label(root, text="Source Path")
    source_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=source_text)
    source_dialogue = ttk.Button(root, image=folder_icon, text="Choose", compound=tk.LEFT, command=lambda: dialog_box_button_action(action="Source"))

    target_input_label = ttk.Label(root, text="Target Path")
    target_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=target_text)
    target_dialogue = ttk.Button(root, image=folder_icon, text="Choose", compound=tk.LEFT, command=lambda: dialog_box_button_action(action="Target"))

    seed_input_label = ttk.Label(root, text="Seed")
    seed_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=seed_text)
    seed_validate = ttk.Button(root, image=random_icon, text="Random", compound=tk.LEFT, command=lambda: seed_text.set(str(random.randint(0, pow(2, 32)))))

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=5, pady=10, sticky=DEFAULT_STICKY)

    # Bottom Level
    button_frame = ttk.Frame(root)
    button_frame.columnconfigure(index=1, weight=5)
    button_frame_left = ttk.Frame(button_frame)
    button_frame_right = ttk.Frame(button_frame)

    # buttons
    seed_file_button = ttk.Button(button_frame_left, text="Seed History", command=lambda:note_tkinter_window("SEED"))
    filter_file_button = ttk.Button(button_frame_left, text="Filter File", command=lambda:note_tkinter_window("FILTER"))
    log_file_button = ttk.Button(button_frame_left, text="Log", command=lambda:note_tkinter_window("LOG"))

    # checkbox
    log_checkbox = ttk.Checkbutton(button_frame_right, text="Make Logs", variable=make_log_bool)
    save_settings_checkbox = ttk.Checkbutton(button_frame_right, text="Save Configuration", variable=save_config_bool)

    # Target Button
    target_button = ttk.Button(root, text="RANDOMISE TEXTURES", style="Export.TButton", image=export_icon, compound=tk.LEFT, command=lambda:pressed_ranomise_button(config_data = config_data))

    # PLACING ALL ELEMENTS DOWN
   
   # Top Bar
    title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=30, sticky='EW')
    about_button.grid(row=0, column=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, ipadx=10, ipady=10, sticky=DEFAULT_STICKY)
   
   # Mid Bar
    source_input_label.grid(row=2, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    source_input.grid(row=2, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    source_dialogue.grid(row=2, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    target_input_label.grid(row=3, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    target_input.grid(row=3, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    target_dialogue.grid(row=3, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    seed_input_label.grid(row=4, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    seed_input.grid(row=4, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    seed_validate.grid(row=4, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    button_frame.grid(row=6, column=0, columnspan=5, sticky=DEFAULT_STICKY)
    button_frame_left.grid(row=0, column=0, columnspan=2, sticky=DEFAULT_STICKY)
    button_frame_right.grid(row=0, column=2, columnspan=2, sticky=DEFAULT_STICKY)

    seed_file_button.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    filter_file_button.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    log_file_button.grid(row=0, column=2, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    log_checkbox.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    save_settings_checkbox.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    target_button.grid(row=7, column=0, columnspan=5, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, ipadx=25, ipady=10, sticky=DEFAULT_STICKY)

    root.mainloop()

# This is to ensure the program is run as a separate file and not a package
if __name__ == "__main__":
    main()                                                  # calls on main function