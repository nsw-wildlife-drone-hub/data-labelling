# data-labelling
### 1. Clone repository
Run the command
```bash
git clone https://github.com/nsw-wildlife-drone-hub/data-labelling.git
```
Or alternatively manually download the code.

### 2. Download Data
***Work in progress***
Download the data from where the data is. Yet to be properly determined. For now it is the YOLOTrainingData directory.

1. Create a new folder that uses the convention *YYYYMMDD_DJI_UUUU/*. Omit any location or pilot name information as the date & ID are the unique identifiers

### 3. Labelling
1. Open DarkLabel
2. Click 'Open Video'
3. Maximize the window panel (this will give fine control of the mouse)
4. Scroll to when the Koala first appears
5. Create a label
  - Left-click: draw a box
  - Shift+Right-click: delete box
  - Shift+Left-click: adjust box
  - Enter: predict next box
6. Save your Ground-truths (GT) by clicking 'GT Save As'

#### 3.1 Good vs bad labels

1. **Make tight boxes:** make the borders of the box touch the object, don't leave white space and definitely don't crop the object
2. **Do not abuse the predict tool:** it can save a lot of time but be sure to 'reset' the label manually after a number of frames so inaccuracies do not compound
3. **Label occluded objects:** if the object is partially hidden, ask yourself, can I still identify the object given the past, present and future frames?
4. **Take your time:** the accuracy of your label will affect the accuracy of the AI. Take a break if you need it, it will be worth it for everyone.

### 4. Extracting Images

1. Open Command Prompt
2. Use the *cd* command to navigate to this directory
3. Use either the .exe or .py:
```bash
extract_frames.exe [Video File] [Frame Folder]
# [Video File]: 20210607_DJI_0020.MP4
# [Frame Folder]: 20210607_DJI_0020
```



***Work in progress***
I will modify this so that not only the images are extracted, but also a full definition video

### 5. Compress labels
1. WinRAR the folder. Right-click ->WinRAR->Add to archive..

2. Change Compression method to ‘Best’

### 6. Upload data

1. Upload the compressed folder to the **Data/** folder in Gdrive

2. Upload the _gt.mp4 data to the **Review/** folder in Gdrive

3. Upload the _clip.mp4 data to the **Clip/** folder in Gdrive

4. Upload the metadata.yaml to the **Metadata/** folder in Gdrive
