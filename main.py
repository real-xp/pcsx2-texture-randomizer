'''
XP's Texture Randomiser Script
'''

import os
import random
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo, showwarning
import webbrowser
import json
import subprocess

# variables global

TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)
SEED = "" # PUT YOUR SEED HERE, wait that sounds wrong, i mean PUT THE SEED FOR THE RANDOMISER HERE
SOURCE_PATH = "./textures/" # This is the path for source textures
FINAL_PATH = "./replacements/" # this is the path where all textures will be moved
LOG = False # set True or False if you want log.txt file generated
CONFIG = False

DEFAULT_FONT = ("Helvetica", 12)
DEFAULT_FONT_NOTEPAD = ("Helvetica", 11)
DEFAULT_FONT_LABEL = ("Helvetica", 12, "bold")
DEFAULT_PADDING = 10
DEFAULT_STICKY = "EW"

file_list = []
# ---

extension_file_array = {}

# this function does exactly that
def get_file_list():
    # filter files

    filter_file_list = []

    try:
        with open("./filter.txt", 'r') as filter_file:
            filter_file_list = [line.strip() for line in filter_file]
    except:
        showwarning(title="Filter List", message="Filter List Not Found", detail="Filter List was not found or does not exist.")

    for file in file_list: # for loop to loop through files
        try:
            file_name, extension = os.path.splitext(file) # splits filename and extension
        except:
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
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
        # print("\n---\tSource Path Valid\t---\n")
        if (os.path.exists(FINAL_PATH)):
            # print("\n---\tFinal Path Valid\t---\n")
            return 0
        else:
            # print("\n---\tFinal Path Invalid. Making New Folder Based On Path\t---\n")
            showinfo(title="Target Folder", message="Target Folder Not Found", detail="A new target folder will be made.")
            try:
                os.mkdir(FINAL_PATH)
                return 0
            except:
                # print("\n---\tError Making Folder For Final Path\t---\n")
                showerror(title="Target Folder", message="Target Folder Could Not Be Made")
                return -1
    else:
        # print("\n---\tSource Path INVALID\t---\n")
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
        return -1

# rename files of specific extension
def rename_spec_ext():

    value_list_size = 0

    if (not extension_file_array):
        # print("\n---\tFile Replacements Not Possible. No Files Detected!\t---\n")
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        progress_log_window()
        for extension, value_list in extension_file_array.items(): # loop through list, giving extension, value of extension in dict
            randomised_list = value_list.copy() # copy into randomised list
            random.shuffle(randomised_list) # shuffles
            value_list_size = len(value_list)

            for index, file_name in enumerate(value_list):
                try:
                    original_file_path = os.path.join(SOURCE_PATH, file_name+extension)
                    renamed_file_path = os.path.join(FINAL_PATH, randomised_list[index]+extension)

                    log_text = f"Renaming {original_file_path}\nTO\n{renamed_file_path}"
                    log_text_label.config(state="normal")
                    log_text_label.insert(tk.END, f"{log_text}\n\n")

                    # progress bar
                    current_progress = (index / value_list_size)
                    progress_bar['value'] = current_progress
                    progress_bar_var.set(f"{current_progress*100}% - {index+1} / {value_list_size}")

                    print (log_text)
                    if (LOG):
                        is_first_time = False
                        if (index == 0):
                            is_first_time = True
                        log_file(is_first_time, log_text)
                    os.rename(original_file_path, renamed_file_path)
                except:
                    print("\n---\tError Renaming And Moving File From Source To Final Path\t---\n")
                    showerror(title="Error Replacing", message="Files could not be replaced")
        print("\n---\tFile Replacements Done!\t---\n")
        log_text_label.config(state="disabled")
        progress_bar['value'] = 100
        progress_bar_var.set(f"100% - {value_list_size} / {value_list_size}")
        showinfo(title="Successful", message="Files were successfully randomised")
        reset_variables()

def make_config_file(data):
    try:   
        with open("./config.json", 'w') as config_file:
            json.dump(data, config_file)
    except FileNotFoundError:
        print("Error: The file 'config.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file.")

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

def set_config_variables(config_data):
    global SOURCE_PATH, FINAL_PATH, SEED, LOG, CONFIG
    SOURCE_PATH = source_text.set(config_data["source_path"])
    FINAL_PATH = target_text.set(config_data["final_path"])
    SEED = seed_text.set(config_data["seed"])
    LOG = make_log_bool.set(config_data["make_log_file"])
    CONFIG = save_config_bool.set(config_data["make_config_file"])

# crypto miner, jk, this just notes the seeds in the seeds.txt file with timestamps
def seed_txt(seed):
    try:   
        with open("./seeds.txt", 'a') as seeds_file:
            seeds_file.write(f"{TIMESTAMP} -> {seed}\n")
    except FileNotFoundError:
        print("Error: The file 'seeds.json' was not found.")

def log_file(first_time, string_file):
    try:   
        with open("./log.log", 'a') as log_file:
            if (first_time):
                log_file.write(f"\n------{TIMESTAMP}------\n\n")
            log_file.write(f"{string_file}\n")
    except FileNotFoundError:
        print("Error: The file 'log.log' was not found.")

def reset_variables():
    global SOURCE_PATH, FINAL_PATH, SEED, file_list
    SOURCE_PATH = source_text.set("")
    FINAL_PATH = target_text.set("")
    SEED = seed_text.set("")
    file_list = []

# ---
# TKINTER WINDOW

def choose_random_seed():
    seed_text.set(str(random.randint(0, pow(2, 32))))

def refresh_progress_window():
    log_window.update()

def progress_log_window():
    global log_window
    log_window = tk.Toplevel(root)
    log_window.title("Executing")
    log_window.geometry("900x450")
    log_window.resizable(0,0)

    log_main_frame = tk.Frame(log_window)
    log_main_frame.pack(fill='both', expand=True)

    log_text_label_scroll = tk.Scrollbar(log_main_frame)
    log_text_label_scroll.pack(fill="y", side='right')

    global log_text_label, progress_bar
    log_text_label = tk.Text(log_main_frame, state="disabled")
    log_text_label.pack(expand=True, fill="both", side='left')  

    log_text_label['yscrollcommand']=log_text_label_scroll.set
    log_text_label_scroll.config(command=log_text_label.yview)

    progress_bar = ttk.Progressbar(log_window, orient='horizontal', mode='determinate')
    progress_bar.pack(expand=True, fill='x', padx=5)
    progress_bar_label = ttk.Label(log_window, text="0%", textvariable=progress_bar_var)
    progress_bar_label.pack(expand=True, fill='x', padx=5)

def open_github_button_action():
    webbrowser.open("https://gist.github.com/real-xp/e9f5b9bb9f416043a9f7dc6e9ab3a7f6#file-readme-md")

def dialog_box_button_action(action):
    dialog_path = filedialog.askdirectory(title="Choose A {action} Path")
    if (dialog_path != ""):
        if (action == "Source"):
            source_text.set(dialog_path)
        elif (action == "Target"):
            target_text.set(dialog_path)

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
    print("Pressed")
    # Multiple Checks
    if (source_text.get() != ""):
        if (target_text.get() != ""):
            if (source_text.get() != target_text.get()):
                print("ok")

                # set path values
                global SOURCE_PATH, FINAL_PATH, SEED, LOG, CONFIG
                SOURCE_PATH = source_text.get()
                FINAL_PATH = target_text.get()
                SEED = seed_text.get()
                LOG = make_log_bool.get()
                CONFIG = save_config_bool.get()

                # testing if filelist can even be detected
                global file_list
                try:
                    file_list = os.listdir(path=SOURCE_PATH)
                except:
                    print("\n---\tError Detecting Files\t---\n")
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
                    make_config_file(config_data)


                if (file_list != []):
                    if (SEED != ''):
                        random.seed(SEED)
                        seed_txt(SEED)
                    else:
                        temp_rand_seed = str(random.randint(0, pow(2, 32)))
                        random.seed(temp_rand_seed)
                        seed_txt(temp_rand_seed)

                    if (check_path_validity() == 0):
                        get_file_list()
                        rename_spec_ext()
                    else:
                        print("\n---\tExiting Program!\t---\n")
                        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")

            else:
                showerror(title="Error",message="Source and Target Paths Conflict" , detail="Source and Target Paths cannot be same.")
        else:
            showerror(title="Error",message="Target Path Empty" , detail="Target path is empty. Please fill in the path.")
    else:
        showerror(title="Error",message="Source Path Empty" , detail="Source path is empty. Please fill in the path.")

def main():
    global root

    root = tk.Tk()
    root.title("PCSX2 Texture Randomiser")
    root.geometry("900x450")
    root.resizable(0,0)

    root.style = ttk.Style(root)
    root.style.configure('TLabel', font=DEFAULT_FONT_LABEL)
    root.style.configure('TButton', font=DEFAULT_FONT_LABEL)
    root.style.configure('TCheckbutton', font=DEFAULT_FONT_LABEL)
    root.style.configure("Export.TButton", font = ("Helvetica", 16, "bold"))
    root.style.configure("Save.TButton", font=DEFAULT_FONT_LABEL)

    root.columnconfigure(index=1, weight=5)

    github_icon = tk.PhotoImage(file='./assets/github.png')
    folder_icon = tk.PhotoImage(file='./assets/folder.png')
    random_icon = tk.PhotoImage(file='./assets/random.png')
    export_icon = tk.PhotoImage(file='./assets/export.png')

    # VARIABLES

    global source_text, target_text, seed_text, make_log_bool, save_config_bool, progress_bar_var

    source_text = tk.StringVar()
    target_text = tk.StringVar()
    seed_text = tk.StringVar()
    make_log_bool = tk.BooleanVar()
    save_config_bool = tk.BooleanVar()
    progress_bar_var = tk.StringVar()

    config_data = read_config_file()
    if (config_data != {}):
        set_config_variables(config_data=config_data)   

    # topbar
    title_label = ttk.Label(root, text="PCSX2 Texture Randomiser", font=("Helvetica", 22, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=30, sticky='EW')
    about_button = ttk.Button(root, image=github_icon, command=open_github_button_action)
    about_button.grid(row=0, column=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, ipadx=10, ipady=10, sticky=DEFAULT_STICKY)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=(0, 20), sticky=DEFAULT_STICKY)

    source_input_label = ttk.Label(root, text="Source Path")
    source_input_label.grid(row=2, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    source_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=source_text)
    source_input.grid(row=2, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    source_dialogue = ttk.Button(root, image=folder_icon, text="Choose", compound=tk.LEFT, command=lambda: dialog_box_button_action(action="Source"))
    source_dialogue.grid(row=2, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    target_input_label = ttk.Label(root, text="Target Path")
    target_input_label.grid(row=3, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    target_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=target_text)
    target_input.grid(row=3, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    target_dialogue = ttk.Button(root, image=folder_icon, text="Choose", compound=tk.LEFT, command=lambda: dialog_box_button_action(action="Target"))
    target_dialogue.grid(row=3, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    seed_input_label = ttk.Label(root, text="Seed")
    seed_input_label.grid(row=4, column=0, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky='w')
    seed_input = ttk.Entry(root, font=DEFAULT_FONT, textvariable=seed_text)
    seed_input.grid(row=4, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    seed_validate = ttk.Button(root, image=random_icon, text="Random", compound=tk.LEFT, command=choose_random_seed)
    seed_validate.grid(row=4, column=2, columnspan=3, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=5, column=0, columnspan=5, pady=10, sticky=DEFAULT_STICKY)

    button_frame = ttk.Frame(root)
    button_frame.columnconfigure(index=1, weight=5)
    button_frame.grid(row=6, column=0, columnspan=5, sticky=DEFAULT_STICKY)

    button_frame_left = ttk.Frame(button_frame)
    button_frame_left.grid(row=0, column=0, columnspan=2, sticky=DEFAULT_STICKY)

    button_frame_right = ttk.Frame(button_frame)
    button_frame_right.grid(row=0, column=2, columnspan=2, sticky=DEFAULT_STICKY)

    # buttons
    seed_file_button = ttk.Button(button_frame_left, text="Seed History", command=lambda:note_tkinter_window("SEED"))
    seed_file_button.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    filter_file_button = ttk.Button(button_frame_left, text="Filter File", command=lambda:note_tkinter_window("FILTER"))
    filter_file_button.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    log_file_button = ttk.Button(button_frame_left, text="Log", command=lambda:note_tkinter_window("LOG"))
    log_file_button.grid(row=0, column=2, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    # checkbox
    log_checkbox = ttk.Checkbutton(button_frame_right, text="Make Logs", variable=make_log_bool)
    log_checkbox.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
    save_settings_checkbox = ttk.Checkbutton(button_frame_right, text="Save Configuration", variable=save_config_bool)
    save_settings_checkbox.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

    target_button = ttk.Button(root, text="RANDOMISE TEXTURES", style="Export.TButton", image=export_icon, compound=tk.LEFT, command=lambda:pressed_ranomise_button(config_data = config_data))
    target_button.grid(row=7, column=0, columnspan=5, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, ipadx=25, ipady=10, sticky=DEFAULT_STICKY)

    root.mainloop()

if __name__ == "__main__":
    main()