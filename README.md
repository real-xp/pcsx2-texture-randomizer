# PCSX2 Texture Randomizer
This is a simple script I made to randomize texture dumps from PCSX2.
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
- Download the textures you want to randomize
    - Make sure the textures you want to randomize are in a separate folder to your `replacements` folder
- Open the `main.py` using Python
- It should bring out a GUI interface
- In `Source Path` field, press `Choose` and select the directory where your textures are located
- In `Target Path` field, press `Choose` and select the directory where you want to rename and move the textures to

## Seeds
- To change the seed for the randomizer, you have multiple options
    - If you leave the `Seed` field empty, it will choose a random seed
    - If you click `Random` next to the `Seed` field, it will give you a random seed
    - You can input any text in the `Seed` field for a custom seed
        - For example, `694202167`, or `Genius Turismo 4` or `IWinChicane2` or `House In The Mountains that John built`
- The seed will also be saved in a `seeds.txt` file, stored in the same directory as `main.py`, which can be accessed via `Seed History` button

## Settings
- You can see all the settings by pressing the `Settings` button on the top right of the main window

### Logging
- You can enable logging of textures to see which textures is renamed to which
- You can enable this by checking the `Make Logs` checkbox
- The log will be saved in a `log.log` file, which will be stored alongside `main.py`
- You can access logs by clicking on the `Open` button
- You can delete logs by pressing `Delete` button

### Filter List
- To add exception / filter for text textures, just include the `filter.txt` file in the same directory as the `main.py`
- You can also choose your own filter file or create one by pressing `Choose` or `Open` in the `Filter` section of `Settings`
    - It will open a Notepad file, where you can paste the texture names
    - Make sure the file names in the `filter.txt` is separated by new lines
    - Please only input the file names in the list, and not the entire paths for the files

### Saving Settings
- You can save settings for the setup by checking the `Save Settings` button
- This will include
    - Source Path
    - Target Path
    - Filter Path
    - Seed
    - Data for both checkboxes
- When you click `Save Settings` button and it performs everything successfully, it will store the configuration in a `config.json` file, located alongside the `main.py` file
- Next time you load the program, it will load the settings
- To delete the configuration, just delete the `config.json`, or click on `Clear Settings`

### GitHub Button
- There is a "GitHub" button to access this `readme.md` file

## Image Dupe
- This will allow you to set a single image or a pool of images as the texture for the entire game
- Click on `Choose` in the `Image Dupe` section in main window, and choose your image file(s)
- Check the `Use` checkbox alongside it
- It will create hard links for that image file in the `Target` folder
  
### Warnings
- Using Image dupe comes with a lot of risks
- As Windows only allows 1024 Hard links per file, where 1 is for the original file itself, the duping function makes temproary files in a temproary folder, just to make more hard links
- Hard links are not supported on a `FAT32` file system
- Hard links are not supported across different partitions of a drive
- Hard links, that might be in the `Recycling Bin` also count towards the limit. It is recommended you permanantly delete the files when deleting them

## Randomize Texture Button
- After everything is filled in, you can press the `Randomize Textures` or `Duplicate Textures` button
- In the command line, it will show you your progress
- After the randomization process is done, you will get a message saying the same

## PCSX2 Setup
- After the script is finished, it should move the textures from the `dumps` folder to the `replacements` folder
- To see the changes, in PCSX2
    - Go to `Settings > Grahpics > Texture Replacements > Load Textures`
    - When you boot the game, you should see randomized textures
- To rerun the script or rerandomize the content, move the textures back to `dumps` folder and follow the steps again 

# Revert Textures
- To rever the textures back to normal, you can
    - Either delete the `replacements` folder where the textures are
    - Turn off `Load Textures` in PCSX2 Graphics Settings

# About
This script was made by `real-xp`, better know as `XP`, along with help from `Azullia`. If you find any flaw or bugs, please tell me in the comment feature of gists.