# PCSX2 Texture randomizer
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
        - For example, `694202167`, or `Genius Turismo 4` or `IWinChicane2` or `House In The Mountains`
- The seed will also be saved in a `seeds.txt` file, stored in the same directory as `main.py`, which can be accessed via `Seed History` button

## Logging
- You can enable logging of textures to see which textures is renamed to which
- You can enable this by checking the `Make Logs` checkbox
- The log will be saved in a `log.log` file, which will be stored alongside `main.py`
- You can access logs by clicking on the `Log` button

## Filter List
- To add exception / filter for text textures, just include the `filter.txt` file in the same directory as the `main.py`
- You can also create or access a brand new `filter.txt` file by clicking on the `Filter File` button
    - It will open a Notepad file, where you can paste the texture names
    - Make sure the file names in the `filter.txt` is separated by new lines
    - Please only input the file names in the list, and not the entire paths for the files

## Saving Configuration
- You can save configuration for the setup by checking the `Save Configuration` checkbox
- This will include
    - Source Path
    - Target Path
    - Seed
    - Data for both checkboxes
- When you click `Randomize Textures` button and it performs everything successfully, it will store the configuration in a `config.json` file, located alongside the `main.py` file
- Next time you load the program, it will load the configuration
- To delete the configuration, just delete the `config.json`

## About Button
- There is a big "GitHub" button on top-right of the window
- It will take you to this `readme.md` file

## Randomize Texture Button
- After everything is filled in, you can press the `Randomize Textures` button
- It will open a new window, where it will show the current progress the renaming process has made
- After the randomization process is done, you can see a temproary log, after which you can close the window

## PCSX2 Setup
- After the script is finished, it should move the textures from the `dumps` folder to the `replacements` folder
- To see the changes, in PCSX2
    - Go to `Settings > Grahpics > Texture Replacements > Load Textures`
    - When you boot the game, you should see randomized textures
- To rerun the script or rerandomize the content, move the textures back to `dumps` folder and follow the steps again 

# About
This script was made by `real-xp`, better know as `XP`, along with help from friends. If you find any flaw, please tell me in the comment feature of gists.