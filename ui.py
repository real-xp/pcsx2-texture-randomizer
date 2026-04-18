import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo
import webbrowser

# ---

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
    note_window = tk.Toplevel(root)
    note_window.title(f"{type_of_action} Window")
    note_window.geometry("450x450")
    note_window.resizable(0,0)

    scroll_text_box = scrolledtext.ScrolledText(note_window, font=DEFAULT_FONT_NOTEPAD)
    scroll_text_box.pack(fill="both")

    button_frame_note_window = ttk.Frame(note_window)
    button_frame_note_window.pack(fill="x")
    button_frame_note_window.columnconfigure(index=(0,1), weight=1)

    clear_button = ttk.Button(button_frame_note_window, text="Clear", style="Save.TButton")
    clear_button.grid(row=0, column=0, ipady=5, sticky="EW")
    save_button = ttk.Button(button_frame_note_window, text="Save", style="Save.TButton")
    save_button.grid(row=0, column=1, ipady=5, sticky="EW")

def pressed_ranomise_button():
    print("Pressed")
    # Multiple Checks
    # Check if Any Path is empty
    if (source_text.get() != ""):
        if (target_text.get() != ""):
        # Check If Paths Are Same
            if (source_text.get() != target_text.get()):
                print("ok")
                progress_log_window()
            else:
                showerror(title="Error",message="Source and Target Paths Conflict" , detail="Source and Target Paths cannot be same.")
        else:
            showerror(title="Error",message="Target Path Empty" , detail="Target path is empty. Please fill in the path.")
    else:
        showerror(title="Error",message="Source Path Empty" , detail="Source path is empty. Please fill in the path.")

def progress_log_window():
    log_window = tk.Toplevel(root)
    log_window.title("Executing")
    log_window.geometry("600x450")
    log_window.resizable(0,0)

    log_text_label = tk.Text(log_window, wrap=tk.WORD, state="disabled")
    log_text_label.pack(expand=True, fill="both")

    progress_bar = ttk.Progressbar(log_window, orient='horizontal', mode='determinate')
    progress_bar.pack(expand=True, fill='x', padx=5)
    progress_bar_label = ttk.Label(log_window, text="0%")
    progress_bar_label.pack(expand=True, fill='x', padx=5)

# ---


DEFAULT_FONT = ("Helvetica", 12)
DEFAULT_FONT_NOTEPAD = ("Helvetica", 11)
DEFAULT_FONT_LABEL = ("Helvetica", 12, "bold")
DEFAULT_PADDING = 10
DEFAULT_STICKY = "EW"

root = tk.Tk()
root.title("PCSX2 Texture Randomiser")
root.geometry("900x450")
# root.minsize(700, 450)
# root.maxsize(900, 450)
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

source_text = tk.StringVar()
target_text = tk.StringVar()
seed_text = tk.StringVar()
make_log_bool = tk.BooleanVar()
save_config_bool = tk.BooleanVar()

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
seed_validate = ttk.Button(root, image=random_icon, text="Random", compound=tk.LEFT)
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
seed_file_button = ttk.Button(button_frame_left, text="Seed History", command=lambda:note_tkinter_window("Seed"))
seed_file_button.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
filter_file_button = ttk.Button(button_frame_left, text="Filter File", command=lambda:note_tkinter_window("Filter"))
filter_file_button.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
log_file_button = ttk.Button(button_frame_left, text="Log", command=lambda:note_tkinter_window("Log"))
log_file_button.grid(row=0, column=2, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

# checkbox
log_checkbox = ttk.Checkbutton(button_frame_right, text="Make Logs", variable=make_log_bool)
log_checkbox.grid(row=0, column=0, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)
save_settings_checkbox = ttk.Checkbutton(button_frame_right, text="Save Configuration", variable=save_config_bool)
save_settings_checkbox.grid(row=0, column=1, columnspan=1, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, sticky=DEFAULT_STICKY)

target_button = ttk.Button(root, text="RANDOMISE TEXTURES", style="Export.TButton", image=export_icon, compound=tk.LEFT, command=lambda:pressed_ranomise_button())
target_button.grid(row=7, column=0, columnspan=5, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING, ipadx=25, ipady=10, sticky=DEFAULT_STICKY)


root.mainloop()