import os
import sys
import argparse
import time
import numpy as np


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = BASE_DIR
sys.path.append(os.path.join(ROOT_DIR, 'TextCondRobotFetch/pointnet'))
from TextCondRobotFetch.pointnet.inference import get_text_model, inference, add_shape_arguments

parser = argparse.ArgumentParser()
add_shape_arguments(parser)
FLAGS = parser.parse_args()


def monitor_bbox_folder(txt_path="selected_bbox_folder_path.txt", result_file="result.txt"):
    while True:
    	  time.sleep(0.1)
    	  if os.path.exists(txt_path):
            with open(txt_path, "w") as f:
                line = f.read().strip()
            result_path = os.path.join(line, result_file)
            if os.path.exists(result_path):
                continue
        break
    return line
        
        
def wait_until_can_read(selected_bbox_folder):
	 prev = 0
	 curr = len(os.listdir(selected_bbox_folder))
    while curr != 0 and prev != curr:
    	 time.sleep(1)
    	 prev, curr = curr, len(os.listdir(selected_bbox_folder))
    return curr
	
	
def pred_shape(selected_bbox_folder, model, latent_folder="TextCondRobotFetch/embeddings", latent_fmt="shape_{:04d}.npy", latent_id=0, result_file="result.txt", npy_fmt="{:03d}.npy"):
    result_file_path = os.path.join(selected_bbox_folder, result_file)
    latent_path = os.path.join(latent_folder, latent_fmt.format(latent_id))
    n = len(os.listdir(selected_bbox_folder))
    latent = np.load(latent_path)
    preds = []
    with open(result_file_path, 'a') as f:
        for i in range(n):
    	      pcd_path = os.path.join(selected_bbox_folder, npy_fmt.format(i))
    	      pcd = np.load(pcd_path)
        	   res = inference(pcd, latent, model)
        	   preds.append(res)
        	   f.write('1' if res else '0')
    return preds
	
	
if __name__ == "__main__":
    shape_model = get_text_model(FLAGS)
    print("monitoring bbox folder")
    selected_bbox_folder = monitor_bbox_folder()
    print("waiting bbox folder")
    n_bbox = wait_until_can_read(selected_bbox_folder)
    print("got {} bboxes".format(n_bbox))
    pred_shape(selected_bbox_folder)
    pass
