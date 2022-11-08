import yaml
import os
from pathlib import PurePath, Path
from cv2 import rectangle, putText
from cv2 import VideoCapture, imwrite
from cv2 import VideoWriter, VideoWriter_fourcc
from tqdm import tqdm
from threading import Thread
from queue import Queue
from glob import glob

# Default config
default_config = {"CAP_PROP_FRAME_WIDTH": 3,
          "CAP_PROP_FRAME_HEIGHT": 4,
          "CAP_PROP_FPS": 5,
          "VID_REGEX": '*DJI*',
          "VIDEO_SUFFIX": '*.MP4',
          "IMG_SUFFIX": '.jpg',
          "OUTPUT_SUFFIX": '_output.mp4',
          "OUTPUT_GT_SUFFIX": '_output_gt.mp4',
          "DRONE_CLASSES": ["koala", "glider", "bird", "macropod", "pig", "deer", "rabbit", "bandicoot", "horse", "fox"]
           }

def load_yaml(file_path, folder=None):
    if file_path in os.listdir():
        with open(file_path, 'r') as f:
            yaml_contents = yaml.safe_load(f)
    else:
        raise FileNotFoundError(f'{file_path} file not found. Please make sure that {file_path} is present in the DarkLabel folder and up to date. This can be downloaded from the GitHub repository.')
    return yaml_contents

def has_ext(folder, extension='.txt'):
    ext_set = set(os.path.splitext(file)[1] for file in os.listdir(folder))
    return extension in ext_set

def print_fol_status(label_list, status_msg=''):
    print(len(label_list), status_msg)
    print(*label_list, sep="\n")
    print()

def search_data():
    # find DJI directories
    dji_fol_list = glob(f'**/{VID_REGEX}/', recursive=True)

    # check for .txt
    label_list = [fol for fol in dji_fol_list if has_ext(fol)]
    print_fol_status(label_list, "found containing labels.")

    # check for .jpg
    label_list = [fol for fol in label_list if not has_ext(fol, IMG_SUFFIX)]
    print_fol_status(label_list, f"found with no images in {IMG_SUFFIX} format.")

    # find .MP4 files
    vid_list = glob(f'**/{VIDEO_SUFFIX}', recursive=True)
    name_dict = {Path(name).stem:name for name in vid_list}

    # find matching .MP4 name and folder name
    label_dict = {}
    for fol in label_list:
        fol_name = PurePath(fol).name
        if fol_name in name_dict:
            label_dict[fol] = name_dict[fol_name]
    label_list = [fol+' <- '+label_dict[fol] for fol in label_dict]
    print_fol_status(label_list, "found with matching video data.")
    return label_dict

class DataExtractor:
    def __init__(self, video_file, folder, dataset_name):
        self.video_file = video_file
        self.folder = folder
        self.video_name = dataset_name + OUTPUT_SUFFIX
        self.video_gt_name = dataset_name + OUTPUT_GT_SUFFIX

        self.image_queue = Queue(maxsize=1)
        self.video_queue = Queue(maxsize=1)
        self.video_gt_queue = Queue(maxsize=1)

        frame_list = [self.basename(frame) for frame in os.listdir(self.folder) if frame.endswith('.txt')]
        self.frame_list = sorted(frame_list)
        self.bbox_list = [self.read_bbox(bbox) for bbox in self.frame_list]
        self.class_list = DRONE_CLASSES

        cap = VideoCapture(self.video_file)
        self.frame_width = int(cap.get(CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(cap.get(CAP_PROP_FRAME_HEIGHT))
        self.fps = int(cap.get(CAP_PROP_FPS))
        cap.release()

    def basename(self, name):
        name = os.path.splitext(name)[0]
        return int(name)

    def write_images(self):
        for f_idx in self.frame_list:
            img = self.image_queue.get(timeout=3)
            img_name = os.path.join(self.folder, str(f_idx).zfill(8))+IMG_SUFFIX
            imwrite(img_name, img)
        return None

    def read_frames(self):
        cap = VideoCapture(self.video_file)
        count = 0
        for frame in tqdm(self.frame_list):
            if frame != count:
                cap.set(1, frame)
                count = frame
            img = cap.read()[1]
            count += 1
            self.image_queue.put(img)
            self.video_queue.put(img.copy())
            self.video_gt_queue.put(img.copy())

        cap.release()
        return None

    def read_bbox(self, file_name):
        text_file = str(file_name).zfill(8)+'.txt'
        with open(self.folder+'/'+text_file, "r") as f:
            contents = f.read()
        bbox_list = [bbox for bbox in contents.split("\n") if bbox]
        return bbox_list

    def convert_bbox(self, bbox):
        c, x, y, w, h = map(eval, bbox.split(' '))
        xmin = int(round((x - w / 2) * self.frame_width))
        xmax = int(round((x + w / 2) * self.frame_width))
        ymin = int(round((y - h / 2) * self.frame_height))
        ymax = int(round((y + h / 2) * self.frame_height))
        return c, (xmin, ymin), (xmax, ymax)

    def add_gt(self, target_frame, idx):
        bbox_list = self.bbox_list[idx]
        for bbox in bbox_list:
            c, xy1, xy2 = self.convert_bbox(bbox)
            label_class = self.class_list[c]
            white = (255, 255, 255)
            pos = (xy1[0], xy1[1] - 5)
            rectangle(target_frame, xy1, xy2, white, 2)
            putText(target_frame, label_class, pos, 0, 0.5, white, 2)
        return target_frame

    def write_video(self, output_name, gt=False):
        frame_dims = (self.frame_width, self.frame_height)
        codec = VideoWriter_fourcc(*"mp4v")
        video = VideoWriter(output_name, codec, self.fps, frame_dims)

        for frame_idx in range(len(self.frame_list)):
            if gt is True:
                vid_frame = self.video_gt_queue.get(timeout=3)
                gt_frame = self.add_gt(vid_frame, frame_idx)
                video.write(gt_frame)
            else:
                vid_frame = self.video_queue.get(timeout=3)
                video.write(vid_frame)

        video.release()
        return None

    def start_threads(self):
        t1 = Thread(target=self.read_frames)
        t2 = Thread(target=self.write_images)
        t3 = Thread(target=self.write_video, args=[self.video_name])
        t4 = Thread(target=self.write_video, args=[self.video_gt_name, True])

        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        return None

if __name__ == "__main__":
    print('Starting dataextract...')
    try:
        config = load_yaml('config.yaml')
        globals().update(config)
    except FileNotFoundError:
        print('Unable to find config.yaml. Continuing with default config.')
        globals().update(default_config)

    print('Searching for data...')
    label_dict = search_data()
    if len(label_dict):
        response = input(f"Would you like to extract data for the above {len(label_dict)} datasets? (Y/N)")
        if response in ['Y', 'y', 'yes', 'Yes', '']:
            for label_path in label_dict:
                video_path = label_dict[label_path]
                dataset_name = PurePath(label_path).name
                print()
                print(f"Extracting data for {dataset_name} dataset...")
                DE = DataExtractor(video_path, label_path, dataset_name)
                DE.start_threads()
            print()
            input("Successfully extracted all available datasets. Press ENTER to finish...")
    else:
        input("No available datasets found to extract. Press ENTER to finish...")
