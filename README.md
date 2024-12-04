<p align="center">
  <img src="https://github.com/Inkdecker/session_drawing/blob/main/ui/resources/icons/sample.png" alt="Project Screenshot" width="400"/>
</p>

# <img src="https://raw.githubusercontent.com/Inkdecker/session_drawing/main/ui/resources/icons/session_drawing.png" width="25" style="vertical-align: middle;" /> Session Drawing

Rework of adnv3k's GestureSesh app :

https://github.com/adnv3k/GestureSesh


This is a free tool to users can use to practice drawing using references from their own libraries.

# New features
	- Ability to save / rename both image and session presets
	- Missing / Deleted files gets removed from presets
	- Autostart session from previous settings
	- Multiple folder selection
	- Zoom functions
	- Grid toggle + Grid settings
	- Copy current image path to clipboard
	- Open current image folder
	- Images cache and large image downscaling
	- Dark / Light themes + Custom themes compatibility
 	- File deletion (Deleted files are send to Recycle Bin)
 	- Image rotation 
  	- Custom shortcuts (Edit the session_settings file, duplicate shortcuts not working)

##### Supported files :  .jpg, .jpeg, .png, .webp, .tiff, .jfif, .bmp


# Usage
[Download](https://github.com/Inkdecker/session_drawing/releases/download/1.1/session_drawing.exe) and run the executable, no installation needed.

1 - Click **"Add Folders"**, then select 1 or more folders containing image files **(.jpg, .jpeg, .png, .webp, .tiff, .jfif, .bmp)** you wish to use for practice.

>Note : You can drag your favorite folders to the left column of the explorer to pin them for a quick access. Right click to remove them.

2 - Create or select a preset with the settings that you want to use for the session.

3 - Click "Start" to begin the session.

>Note: You can select "Randomize" to shuffle the pictures and "Start session" to automatically start the session whenever the program is launched using your latest settings.


## Troubleshooting
- Delete the **session_settings.txt** and restart the executable to reset settings and shortcuts.
- Delete the **preset folder** and restart the executable to reset everything back to default.

- Note : Using images with atypical characters in their filenames might sometimes cause a crash.


## Default Hotkeys
All **hotkeys** can be modified through the **session_settings.txt** inside the preset folder, however, be careful as <ins>duplicate the keys get disabled</ins>.

### Configuration window:
Button | Hotkey
------------ | -------------
Start session | S
Close Window | Escape

### Session Window: 
Button | Hotkey
------------ | -------------
Zoom + | S, Numpad +, Mousewheel
Zoom - | D, Numpad -, Mousewheel
Rotate Right | Q, Ctrl + Mousewheel
Rotate Left | F, Ctrl + Mousewheel
Toggle grid | G
Toggle grid settings | Ctrl + G
Grayscale | T
Flip Horizontal | H
Flip Vertical | V
Toggle Window Resizing (dynamic/static) | R
Toggle Always On Top | A
Toggle Mute | M
Previous Image | Left Arrow Key
Stop | Esc 
Pause | Spacebar
Next Image | Right Arrow Key
Copy image path | Ctrl + C
Open image folder | O
Delete image | Ctrl + D
Open setting window | Tab
Add 30s | Up Arrow Key
Add 1 Minute | Ctrl + Up Arrow Key
Reset timer | Ctrl + Shift + Up Arrow Key

## Licence
[GNU General Public License v3.0](https://github.com/Inkdecker/session_drawing/blob/main/LICENSE)
