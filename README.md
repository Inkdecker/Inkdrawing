# Session_drawing

Rework of adnv3k's GestureSesh app :

https://github.com/adnv3k/GestureSesh


This is a free tool to users can use to practice drawing using references from their own libraries.

# New features
	- Ability to save / rename both image and session presets
	- Missing / Deleted files gets removed from presets
	- Autostart  session from previous settings
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



## Troubleshouting
- Delete the session_settings.txt and restart the executable to reset settings and shortcuts.
- Delete the preset folder and restart the executable to reset everything back to default.


## Default Hotkeys
### Configuration window:
Button | Hotkey
------------ | -------------
Start session | S
Close Window | Escape

### Session Window: 
Button | Hotkey
------------ | -------------
Zoom + | Q, Numpad +, Mousewheel
Zoom - | D, Numpad -, Mousewheel
Rotate Right | S, Ctrl + Mousewheel
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
Copy image path | C
Open image folder | O
Delete image | Ctrl + D
Open setting window | Tab
Add 30s | Up Arrow Key
Add 1 Minute | Ctrl + Up Arrow Key
Reset timer | Ctrl + Shift + Up Arrow Key
