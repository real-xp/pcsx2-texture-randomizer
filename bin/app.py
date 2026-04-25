# importing all requirementrs, does not require pip
import os
import random
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo, showwarning, askyesno
import webbrowser
import subprocess
import variables
import core

# ------------------------------------------------------------
#                   TKINTER CORE FUNCTIONS
# ------------------------------------------------------------

# It resets variables after replacement of all textures is done
def reset_variables():
    try:
        source_text.set("")
        target_text.set("")
        seed_text.set("")
        img_dupe_use_var.set(False)
        img_dupe_var.set("")
        core.file_list = []
        variables.IMG_DUPE_ARRAY = []
        img_dupe_input['values'] = variables.IMG_DUPE_ARRAY
    except Exception as error:
        print(f"{variables.ERROR_CODE}[ERROR]\t Could not reset variables : {error}{variables.END_CODE}")

# opens my github tutorial readme.md
def open_github_button_action():
    webbrowser.open("https://gist.github.com/real-xp/e9f5b9bb9f416043a9f7dc6e9ab3a7f6#file-readme-md")

# dialog box action for folders
def dialog_box_button_action(action : str, type_of_action : str):
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
            variables.FILTER_PATH = dialog_path
            filter_var.set(variables.FILTER_PATH)

# select image pool function
def dialog_box_multi_select_img_dupe():
    dialog_path_array = filedialog.askopenfilenames(title=f"Choose Images", initialdir="./", filetypes=[("PNG", "*.png"), ("DDS", "*.dds"), ("BMP", "*.bmp"), ("All Files", "*")])
    if (dialog_path_array != []):
        variables.IMG_DUPE_ARRAY = dialog_path_array
        img_dupe_input['values'] = variables.IMG_DUPE_ARRAY
            
# Opens Notepad When Button Pressed
def open_notepad_window(path):
    try:
        subprocess.run(["notepad",path])
    except Exception as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tCould not open notepad : {error}{variables.END_CODE}")
        showerror(title="Error", message="Some Kind Of Error Occured")

# deletes file of log and seed
def delete_files(path):
    try:
        os.remove(path)
        showinfo(title="Successful", message="File was successfully deleted.")
    except Exception as error:
        showerror(title="Error", message="Some kind of error occured while deleting.")
        print(f"{variables.ERROR_CODE}[ERROR]\tCould not delete files : {error}{variables.END_CODE}")
        # set variables for use

# randomise button pressed, does checks        
def pressed_ranomise_button():
    # Multiple Checks
    if (source_text.get() == ""):                               # sees if source entry is empty
        showerror(title="Error",message="Source Path Empty" , detail="Source path is empty. Please fill in the path.")
        return
    if (img_dupe_use_var.get()):
        message = "Are you sure you want to continue? This will link the image you chose to multiple files with names from SOURCE folder and put them in TARGET folder"

        if (variables.IMG_DUPE_ARRAY == []):                              # sees if img_dupe entry is empty
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
    variables.SOURCE_PATH = source_text.get()
    variables.FINAL_PATH = target_text.get()
    variables.SEED = seed_text.get()
    variables.LOG = make_log_bool.get()
    variables.SEED_SAVE = make_seed_bool.get()
    variables.FILTER_PATH = filter_var.get()
    variables.ING_DUPE_BOOL = img_dupe_use_var.get()
    variables.TUTORIAL = show_tutorial_bool.get()

# main place where randomisation initially passes checks
def main_randomizer_task(is_image_duping_action : bool):
    # Set variable values
    set_variables()

    # removing \ to use / in path, if user didnt use choose button
    variables.SOURCE_PATH = variables.SOURCE_PATH.replace("\\", "/")
    variables.FINAL_PATH = variables.FINAL_PATH.replace("\\", "/")

    # testing if filelist can even be detected
    try:
        for root, dirs, files in os.walk(variables.SOURCE_PATH):              # parses and recursively gets all files in text
            for n in files:
                fp = os.path.join(root, n)
                ft = fp.replace(variables.SOURCE_PATH, "")
                fl = ft.replace("\\", "/")
                core.file_list.append(fl)
    except Exception as error:
        print(f"{variables.ERROR_CODE}[ERROR]\tCould not detect files : {error}{variables.END_CODE}")
        showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
        core.file_list = []

    # sees if file list is not empty
    if (core.file_list != []):
        if (variables.FILTER_PATH == ""):                                     # checks if filter path is not empty
            variables.FILTER_PATH = "./filter.txt"                            # puts default path link as safety check

        if (variables.SEED == ''):                                            # checks if user left seed input field empty
            variables.SEED = str(random.randint(0, pow(2, 32)))               # chooses random int between 0 and 2**32

        random.seed(variables.SEED)                                           # sets the seed into random pkg

        if (variables.SEED_SAVE):                                             # checks if seed saving is turned on
            core.seed_txt(variables.SEED)                                          # puts the seed into seed history file

        if (core.check_path_validity() == 0):                            # checks if path is valid
            core.get_file_list(core.file_list)                                # calls on file filter and file collector
            if (not is_image_duping_action):
                core.rename_spec_ext()                                   # actual renaming function
            else:
                if (not askyesno(title="Are You SURE?", message="This method invloves making Hard Links from the image file you provided and make thousands of linked files. This approach uses less storage than copying, but has a lot of limitations. Do you still want to continue?")):
                    return
                if (not askyesno(title="Are You REALLY SURE?", message="As windows puts a limit of 1024 hard links including original image file, this program will create multiple temproary files in case of thousands of files. There are more limitations. Do you want to still continue?")):
                    return
                if (not askyesno(title="Are You REALLY REALLY SURE?", message="Hard Links are also not possible on a USB Stick or a partition of a drive formatted with FAT32. This means if your drive is FAT32, please do not continue. Do you still wish to continue")):
                    return
                if (not askyesno(title="Are You REALLY REALLY REALLY SURE?", message="If you have done this process before, and deleted the linked files, but they are still in recycling bin, PLEASE DELETE THOSE FILES AS THEY STILL COUNT AS HARD LINKS AND COUNT TOWARDS THE ORIGINAL IMAGE LIMIT. IF YOU DONT DELETE, THE PROGRAM WILL CRASH AND WILL NOT GENERATE IMAGES. Do you still wish to continue?")):
                    return
                core.set_hard_links()                                    # sets hard links, for image duping
        else:
            showerror(title="Files Not Detected", message="Files could not be detected", detail="Make sure the source path is correct.")
    else:
        showerror(title="Files not detected", message="Files were not detected in source folder", detail="Make sure the source folder is not empty.")
        print(f"{variables.ERROR_CODE}[ERROR]\tCould not detect files{variables.END_CODE}")

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
    seed_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window(variables.SEED_SAVE_PATH))
    seed_file_delete = ttk.Button(settings_window, text="Delete", command=lambda:delete_files(variables.SEED_SAVE_PATH))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=5, padx=variables.DEFAULT_PADDING_X ,pady=(5,0), sticky=variables.DEFAULT_STICKY)

    # Logs section
    logs_title = ttk.Label(settings_window, text="Logs", style="Subtitle.TLabel")
    logs_save_checkbox = ttk.Checkbutton(settings_window, text="Make Logs", variable=make_log_bool)
    logs_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window(variables.LOG_PATH))
    logs_file_delete = ttk.Button(settings_window, text="Delete", command=lambda:delete_files(variables.LOG_PATH))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=5, padx=variables.DEFAULT_PADDING_X ,pady=(5,0), sticky=variables.DEFAULT_STICKY)

    # Filter section
    filter_title = ttk.Label(settings_window, text="Filter", style="Subtitle.TLabel")
    filter_file_title = ttk.Entry(settings_window, state="disabled", textvariable=filter_var)
    filter_file_open = ttk.Button(settings_window, text="Open", command=lambda:open_notepad_window(variables.FILTER_PATH))
    filter_file_choose = ttk.Button(settings_window, text="Choose", command=lambda: dialog_box_button_action(action="Filter", type_of_action="FILE"))

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=9, column=0, columnspan=5, padx=variables.DEFAULT_PADDING_X ,pady=(5,0), sticky=variables.DEFAULT_STICKY)

    # Filter section
    tutorial_title = ttk.Label(settings_window, text="Tutorial", style="Subtitle.TLabel")
    tutorial_file_checkbox = ttk.Checkbutton(settings_window, text="Show tutorial on startup", variable=show_tutorial_bool)
    tutorial_file_open = ttk.Button(settings_window, text="Open Tutorial", command=open_github_button_action)

    ttk.Separator(settings_window, orient=tk.HORIZONTAL).grid(row=12, column=0, columnspan=5, padx=variables.DEFAULT_PADDING_X ,pady=(5,0), sticky=variables.DEFAULT_STICKY)

    # Config section
    about_me = ttk.Label(settings_window, text="Made by realXP (XP)")

    config_file_clear = ttk.Button(settings_window, text="Clear Settings", command=lambda: delete_files(variables.CONFIG_PATH))
    config_file_save = ttk.Button(settings_window, text="Save Settings", command=core.make_config_file)

    # Placing Elements
    # Top Bar
    title_label.grid(row=0, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_X, sticky='EW')

    # Seeds Section
    seed_title.grid(row=1, column=0, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=0, sticky='w')
    seed_save_checkbox.grid(row=2, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    seed_file_open.grid(row=2, column=2, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    seed_file_delete.grid(row=2, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
   
    # Log Section
    logs_title.grid(row=4, column=0, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    logs_save_checkbox.grid(row=5, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    logs_file_open.grid(row=5, column=2, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    logs_file_delete.grid(row=5, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    # Filter Section
    filter_title.grid(row=7, column=0, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    filter_file_title.grid(row=8, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    filter_file_open.grid(row=8, column=2, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    filter_file_choose.grid(row=8, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    # Tutorial Section
    tutorial_title.grid(row=10, column=0, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=(10,0), sticky='w')
    tutorial_file_checkbox.grid(row=11, column=0, columnspan=3, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    tutorial_file_open.grid(row=11, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    # Config Section
    about_me.grid(row=13, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X_SUBTITLE, pady=variables.DEFAULT_PADDING_X_SUBTITLE, sticky=variables.DEFAULT_STICKY)
    config_file_clear.grid(row=13, column=2, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_X_SUBTITLE, sticky=variables.DEFAULT_STICKY)
    config_file_save.grid(row=13, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_X_SUBTITLE, sticky=variables.DEFAULT_STICKY)

# ------------------------------------------------------------
#                   TKINTER WINDOW MAIN
# ------------------------------------------------------------

# main body of the program, this runs the tkinter window
def main():
    global root, source_text, target_text, seed_text, make_log_bool, save_config_bool, make_seed_bool, filter_var, img_dupe_var, img_dupe_use_var, img_dupe_input, target_button, show_tutorial_bool

    # defining root window
    root = tk.Tk()
    root.title("PCSX2 Texture Randomizer")
    root.geometry("900x360")
    root.resizable(False,False)

    # defining styles for ttk widgets
    root.style = ttk.Style(root)
    root.style.configure('TLabel', font=variables.DEFAULT_FONT_LABEL)
    root.style.configure('TButton', font=variables.DEFAULT_FONT_LABEL)
    root.style.configure('TCheckbutton', font=variables.DEFAULT_FONT_LABEL)
    root.style.configure("Export.TButton", font = ("Helvetica", 16, "bold"))
    root.style.configure("Save.TButton", font=variables.DEFAULT_FONT_LABEL)
    root.style.configure("Subtitle.TLabel", font=variables.DEFAULT_FONT_LABEL_SUBTITLE)

    # defining column weight
    root.columnconfigure(index=1, weight=5)

    # VARIABLES
    source_text = tk.StringVar()                                # takes source string from input
    target_text = tk.StringVar()                                # takes target string from input
    seed_text = tk.StringVar()                                  # takes seed from input
    make_log_bool = tk.BooleanVar()                             # takes checkbox boolean value of log
    show_tutorial_bool = tk.BooleanVar()                        # takes checkbox boolean value of tutorial
    make_seed_bool = tk.BooleanVar()                            # takes checkbox boolean value of seed
    filter_var = tk.StringVar()                                 # stores filter_file path
    img_dupe_var = tk.StringVar()                               # stores img_dupe path
    revert_combo_box()
    img_dupe_use_var = tk.BooleanVar()                          # takes checkbox boolean value of img_dupe

    config_data = core.read_config_file()                            # reads the config file
    if (config_data != {}):
        core.set_config_variables(config_data=config_data)           # if config file exists, set values to config file ones
    else:
        show_tutorial_bool.set(True)

    # Top Bar
    title_label = ttk.Label(root, text="PCSX2 Texture Randomizer", font=("Helvetica", 22, "bold"))
    about_button = ttk.Button(root, text="Settings", command=open_settings_window)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=5, pady=(0, 20), sticky=variables.DEFAULT_STICKY)

    # Mid level
    source_input_label = ttk.Label(root, text="Source Path")
    source_input = ttk.Entry(root, font=variables.DEFAULT_FONT, textvariable=source_text)
    source_dialogue = ttk.Button(root, text="Choose", command=lambda: dialog_box_button_action(action="Source", type_of_action="FOLDER"))

    target_input_label = ttk.Label(root, text="Target Path")
    target_input = ttk.Entry(root, font=variables.DEFAULT_FONT, textvariable=target_text)
    target_dialogue = ttk.Button(root, text="Choose", command=lambda: dialog_box_button_action(action="Target", type_of_action="FOLDER"))

    seed_input_label = ttk.Label(root, text="Seed")
    seed_input = ttk.Entry(root, font=variables.DEFAULT_FONT, textvariable=seed_text)
    seed_validate = ttk.Button(root, text="Random", command=lambda: seed_text.set(str(random.randint(0, pow(2, 32)))))

    img_dupe_input_label = ttk.Label(root, text="Image Dupe")
    img_dupe_input = ttk.Combobox(root, textvariable=img_dupe_var, state="readonly", font=variables.DEFAULT_FONT)
    img_dupe_input.bind("<<ComboboxSelected>>", revert_combo_box)
    img_dupe_use = ttk.Checkbutton(root, text="Use", variable=img_dupe_use_var, command=change_text_to_dupe)
    img_dupe_choose = ttk.Button(root, text="Choose", command=dialog_box_multi_select_img_dupe)

    ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=6, column=0, columnspan=5, pady=10, sticky=variables.DEFAULT_STICKY)

    # Target Button
    target_button = ttk.Button(root, text="RANDOMIZE TEXTURES", style="Export.TButton", command=pressed_ranomise_button)

    # PLACING ALL ELEMENTS DOWN
   # Top Bar
    title_label.grid(row=0, column=0, columnspan=2, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_X, sticky='EW')
    about_button.grid(row=0, column=3, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_X_SUBTITLE, ipadx=10, ipady=10, sticky=variables.DEFAULT_STICKY)
   
   # Mid Bar
    source_input_label.grid(row=2, column=0, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky='w')
    source_input.grid(row=2, column=1, columnspan=2, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    source_dialogue.grid(row=2, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    target_input_label.grid(row=3, column=0, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky='w')
    target_input.grid(row=3, column=1, columnspan=2, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    target_dialogue.grid(row=3, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    seed_input_label.grid(row=4, column=0, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky='w')
    seed_input.grid(row=4, column=1, columnspan=2, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    seed_validate.grid(row=4, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    img_dupe_input_label.grid(row=5, column=0, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky='w')
    img_dupe_input.grid(row=5, column=1, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    img_dupe_use.grid(row=5, column=2, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)
    img_dupe_choose.grid(row=5, column=3, columnspan=1, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, sticky=variables.DEFAULT_STICKY)

    target_button.grid(row=7, column=0, columnspan=5, padx=variables.DEFAULT_PADDING_X, pady=variables.DEFAULT_PADDING_Y, ipadx=25, ipady=10, sticky=variables.DEFAULT_STICKY)

    if (show_tutorial_bool.get()):
        if (askyesno(title="Welcome To Texture Randomizer", message="Welcome to Texture Randomizer. Do you want to check out the tutorial on how to use this program? (You can disable this startup message in the Settings)")):
            open_github_button_action()

    root.mainloop()