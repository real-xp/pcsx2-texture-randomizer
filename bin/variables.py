import datetime

# ------------------------------------------------------------
#                       VARIABLES
# ------------------------------------------------------------

# HARD CODED PATHS
SOURCE_PATH = "./textures/"                                 # This is the path for source textures
FINAL_PATH = "./replacements/"                              # this is the path where all textures will be moved
FILTER_PATH = "./filter.txt"                                # This is the path for filter, default path
CONFIG_PATH = "./config.json"                               # This is the path for where config.json file is stored
SEED_SAVE_PATH = "./seeds.txt"                              # This is the path for where seeds.txt file is stored
LOG_PATH = "./log.log"                                      # This is the path for where log.log file is stored
TEMP_DIR_PATH = "./tempfiles"                               # This is the path for where temp files are stored

# PRINT ASCII COLOR CODES
WARNING_CODE = '\033[93m'                                   # Yellow for warning printing
ERROR_CODE = '\033[91m'                                     # Red for warning printing
END_CODE = '\033[0m'                                        # Ends the ascii

# DO NOT CHANGE ON YOUR OWN
TIMESTAMP = datetime.datetime.now(datetime.timezone.utc)    # generates a timestamp of when script is run
SEED = ""                                                   # PUT YOUR SEED HERE, wait that sounds wrong, i mean PUT THE SEED FOR THE RANDOMIZER HERE
LOG = False                                                 # set True or False if you want log.log file generated
TUTORIAL = True                                             # set True or False if you want tutorial shown
SEED_SAVE = False                                           # set True or False if you want seeds.txt generated
IMG_DUPE_ARRAY = []                                         # This is the array for img dupe paths, key = img_path, value = dict of values
ING_DUPE_BOOL = False                                       # This is the bool for img dupe, checks if we want to dupe images or not
HARD_LINK_LIMIT = 1000                                      # Limit for hard links per file
GITHUB_TUTORIAL_LINK = "https://github.com/real-xp/pcsx2-texture-randomizer/blob/main/README.md"    # Where the tutorial file is

# variables for tkinter styling
DEFAULT_FONT = ("Helvetica", 12)
DEFAULT_FONT_LABEL = ("Helvetica", 12, "bold")
DEFAULT_FONT_LABEL_SUBTITLE = ("Helvetica", 14, "bold")
DEFAULT_PADDING_X = 10
DEFAULT_PADDING_X_SUBTITLE = 20
DEFAULT_PADDING_Y = 5
DEFAULT_STICKY = "EW" 

# This is the array that stores the file names including their paths
# This is mainly for temproary reasons to check if the source folder has image files
file_list = []                                              # empty dict initialised before

# This is a dict / map for the files
# The key is the extension for the file
# The value is the path of the file of that particular extension
# This can be used to filter out particular extensions too
extension_file_dict = {}                                   # empty dict initialised before