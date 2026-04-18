# PCSX2 Texture Randomiser
This is a simple script I made to randomise texture dumps from PCSX2.
Initially the script was made just for the purpose of randomising Enthusia (game) textures, but this can be used in many other games

# Requirements
- You need Python 3 installed on your system
- You need `Texture Replacement` enabled on PCSX2
    - To do that, Go to `Settings > Graphics`
    - Under `Graphics`, go to `Texture Replacement`
    - There you should see both your location for texture dumps and replacement, and settings to allow dumping and loading of textures
- The game's texture dump (You can usually download HD textures from the internet like in case of Gran Turismo 4 or Enthusia)

# Usage
To use this script, follow the steps
- Download the `main.py` file
- Download the textures you want to randomise
    - Make sure the textures you want to randomise are in a separate folder to your `replacements` folder
- Put the file in the textures folder of PCSX2, the folder where you see `dumps` and `replacements` folder
    - So like in the case of Enthusia, in `Documents > PCSX2 > textures > SLUS-20967`
    - You should see folder `dumps` and `replacements`
    - Put the `main.py` file next to those folders
- Open `main.py` with Notepad or any text editor
- Search for `SOURCE_PATH` and put the path of the folder where your texture dump is, in between the ""
    - In this case, it can be something like `"C:\Users\XP\Documents\PCSX2\textures\SLUS-20967\dumps"`
    - **NOTE** - Make sure to change the `\` in between the path to the `/`, so it would look like `"C:/Users/XP/Documents/PCSX2/textures/SLUS-20967/dumps"`
- Search for `FINAL_PATH` and put the path of the replacements folder between ""
    - So in this case, something like `"C:\Users\XP\Documents\PCSX2\textures\SLUS-20967\replacements"`
    - **NOTE** - Make sure to change the `\` in between the path to the `/`, so it would look like `"C:/Users/XP/Documents/PCSX2/textures/SLUS-20967/replacemements"`

## Seeds
- To change the seed for the randomiser, you have two options
    - The default seed, if left empty will be based on the timestamp of the system
    - You can set a custom seed by searching for `SEED` in the code, and in between "", putting the seed
- The seed will also be saved in a `seeds.txt` file
- After everything is double checked, run the script using python
    - You can do that by right clicking the `main.py` file, open with `python` and it should run the script
    - You can also open command line and run `python main.py`

## Filter List
- To add exception / filter for text textures, just include the `filter.txt` file in the code
- Make sure the file names in the `filter.txt` is separated by new lines
- Delete all the extension from the files, like `.bmp` or `.dds` for the script to work

## PCSX2 Setup
- After the script is finished, it should move the textures from the `dumps` folder to the `replacements` folder
- To see the changes, in PCSX2
    - Go to `Settings > Grahpics > Texture Replacements > Load Textures`
    - When you boot the game, you should see randomised textures
- To rerun the script or rerandomise the content, move the textures back to `dumps` folder and follow the steps again