from cv2 import VideoCapture, imwrite
import os
from sys import argv
from tqdm import tqdm
from threading import Thread
from queue import Queue

def read_frames(frame_list, video_file, frames_queue):
    cap = VideoCapture(video_file)
    count = 0
    for frame in frame_list:
        if frame != count:
            cap.set(1, frame)
            count = frame
        img = cap.read()[1]
        count += 1
        frames_queue.put(img)

def write_frames(frame_list, folder, frames_queue):
    for frame in tqdm(frame_list):
        img = frames_queue.get(timeout=1)
        imwrite(os.path.join(folder,str(frame).zfill(8))+'.jpg', img)


def read_basename(name):
    name = os.path.splitext(name)[0]
    return int(name)


def check_txt(name):
    if str(name).split('.')[1]=='txt':
        return True
    return False


def extract_frames(video_file, folder):
    frames_queue = Queue(maxsize=1)

    frame_list = [read_basename(frame) for frame in os.listdir(folder) if check_txt(frame)]
    frame_list = sorted(frame_list)

    t1 = Thread(target=read_frames, args=(frame_list, video_file, frames_queue))
    t2 = Thread(target=write_frames, args=(frame_list, folder, frames_queue))

    t1.start()
    t2.start()

    t1.join()
    t2.join()


if __name__=='__main__':
    if len(argv) > 2:
        video_file = argv[1]
        folder = argv[2]
    else:
        raise ValueError('Please enter the correct number of inputs\n1: Video File\n2: Frame Folder')

    extract_frames(video_file, folder)
