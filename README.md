# <img src="https://raw.githubusercontent.com/Inkdecker/Inkdrawing/main/ui/resources/icons/Inkdrawing.png" width="50" style="vertical-align: middle;" /> Inkdrawing

Rework of adnv3k's GestureSesh app :

https://github.com/adnv3k/GestureSesh


This is a free tool to users can use to practice drawing using references from their own libraries.

<p align="center">
  <img src="https://github.com/Inkdecker/Inkdrawing/blob/main/ui/resources/icons/sample.png" alt="Project Screenshot" width="400"/>
</p>

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
	   
	- 04.12.2024: Ability to create Rainmeter profiles to export the slideshows.
	- 30.12.2024: Main functions available from commande line.
	- 28.03.2025: Search function for the image presets.
	- 07.04.2025: Added color labels to the image preset table.
	- 18.04.2025: Renamed from session_drawing to Inkdrawing.
	
	- (New) 29.09.2025: Add images to current preset.
	- (New) 29.09.2025: Auto contrast.

##### Supported files :  .jpg, .jpeg, .png, .webp, .tiff, .jfif, .bmp


# Usage
[Download](https://github.com/Inkdecker/Inkdrawing/releases/latest/download/Inkdrawing.exe) and run the executable, no installation needed.
>Note : The settings, themes and preset files gets stored inside the **"drawing_presets"** folder, this folder gets created upon launch if missing.
 
1 - Click **"Add Folders"**, then select 1 or more folders containing image files **(.jpg, .jpeg, .png, .webp, .tiff, .jfif, .bmp)** you wish to use for practice.

>Note : You can drag your favorite folders to the left column of the explorer to pin them for a quick access. Right click to remove them.

2 - Create or select a preset with the settings that you want to use for the session.

3 - Click "Start" to begin the session.

>Note: You can select "Randomize" to shuffle the pictures and "Start session" to automatically start the session whenever the program is launched using your latest settings.

## Rainmeter
The image preset can be exported and used as rainmeter slideshow. To do so, select the image preset you want to export and press the [Rainmeter] button. You can then place the created profile inside your **"..\RAINMETER\Skins"** folder and then launch it using rainmeter.
> Note: The IMG_SLIDESHOW.ini file can be edited to customise the slideshow. Most variables can be found in the [Variables] section.
> 
> Note: Deleted image files get send to the "..\rainmeter_presets\Deleted Files" folder. 

## Command line
### Create preset
- **create_preset**
  - **`-folder_list` (required)**: Path(s) to the folder(s) containing image files
  - **`-preset_name` (optional)**: Name of the preset |  *Default*: `"preset_output"`
  - **`-output_folder` (optional)**: Folder to save the preset file
 
##### Example :
```batch
Inkdrawing.exe create_preset -folder_list "D:\Desktop\Image_Folder_1" "D:\Desktop\Image_Folder_2" -preset_name "Image_preset_1" -output_folder "D:\Desktop\Output_Folder"
```

### Update preset
- **update_preset**
  - **`-preset_path` (required)**: Path of the preset to update
  - 
##### Example :
```batch
Inkdrawing.exe update_preset -preset_path "D:\Desktop\Image_preset_1.txt"
```

### Start session
- **start_session_from_files**
  - **`-image_preset_path` (required)**: Path to the image preset file
  - **`-session_preset_path` (required)**: Path to the session preset file
  - **`-randomize_settings` (optional)**: Randomize settings (`True`/`False`)  |  *Default*: `True`
 
##### Example :
```batch
Inkdrawing.exe start_session_from_files -image_preset_path "D:\Desktop\Image_preset_1.txt" -session_preset_path "D:\Desktop\Session_preset_1.txt" -randomize_settings True
```



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
Cycle Labels | ²
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

### Rainmeter Slideshow: 
Button | Hotkey
------------ | -------------
Display title | Mousehover
Previous Image | Left click
Next Image | Right click
Open Image File | Middle click
Copy Image File Path | Scroll up
Close slideshow | Scroll down
Move image to "..\rainmeter_presets\Deleted Files" | Mouse button 1
Open Image folder | Mouse button 2

## Licence
[GNU General Public License v3.0](https://github.com/Inkdecker/Inkdrawing/blob/main/LICENSE)
