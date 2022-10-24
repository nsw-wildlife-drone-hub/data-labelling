DarkLabel (Ver2.3 - update2)
 - last modified: Jul. 3, 2021
 - by dark programmer (darkpgmr.lee@gmail.com)
 - http://darkpgmr.tistory.com/16

Main Features
 - Video/image object labeling & annotation tool (bounding box with ID and label)
   . automatic object labeling by visual tracking (multi-target)
   . semi-automatic labeling by linear interpolation
   . user-configurable data formats (pascal voc, darket yolo, xml/txt, any other user-defined formats)
   . user-configurable hotkeys and zoom in / zoom out support
 - Video splitting (into images) & image merging (into a video file) tool
 - Video cropping tool (cut and save only the selected section in the video)
 - Video/image privacy masking tool (mosaic the box area in the image)
 - Windows only (32/64 bits)

How to Use
  darklabel.yml: edit this file to configure the program (data formats, hotkeys, other options, ...)
  
	Arrow/PgUp/PgDn/Home/End: navigate image frames	
	
	Mouse: Left(create box), Right(cancel the most recently created box)
	Shift+Mouse: Left(modify box), Right(delete selected box/trajectory or all boxes)
	Shift+DoubleClick: modify box properties (label, ID, difficulty)
	
	DoubleClick: select/deselect box trajectory
	*box trajectory: boxes connected across frames with the same ID and label
	
	Ctrl+'+'/'-': zoom in/out
	Ctrl+Arrow: scroll zoomed window
	Ctrl+MouseWheel: zoom in/out
	Ctrl+MouseDrag: scroll zoomed window
	
	Enter: apply tracking (selected trajectories or newly created boxes only)
	Ctrl+'s': save gt	
	F1: show help
