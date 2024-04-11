import cv2
import numpy as np
import os
import shutil
import threading
import torch
from datetime import datetime
from decord import VideoReader, cpu
from huggingface_hub import hf_hub_download
from IPython.display import display
from pathlib import Path
from PIL import Image
from transformers import XCLIPProcessor, XCLIPModel
class AutoLabeler():


    def __init__(self):
        # Define the base directory
        base_directory = os.path.dirname(os.path.realpath(__file__))
        self.classes =  ['human is hammering', 'human is measuring', 'human is stacking boxes', 'human is scissoring','human is cutting','human is drilling','no human in scene']
        self.is_recording = True
        self.local_server_ip = "http://146.244.98.19:5000/video_feed" #or any other IP depending on raspberrypi 
        # Define other directories relative to the base directory
        self.save_directory = base_directory
        self.save_directory_full_vids = base_directory + "/full_vids"
        self.save_good_vids_directory = base_directory + "/good_vids"
        # Ensure directories exist
        if not os.path.exists(base_directory + "/outputs"):
            os.makedirs(base_directory + "/outputs")
        if not os.path.exists(self.save_directory_full_vids):
            os.makedirs(self.save_directory_full_vids)
        if not os.path.exists(self.save_good_vids_directory):
            os.makedirs(self.saveoutput_good_vids_directory)
        # Load the model and processor
        self.model_name = "microsoft/xclip-base-patch16-zero-shot"
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.processor = XCLIPProcessor.from_pretrained(self.model_name)
        self.model = XCLIPModel.from_pretrained(self.model_name)
        self.model = self.model.to(self.device)
        self.video_path = self.save_directory + "/outputs/output.mp4"
        self.is_recording = True
        self.video_filename = "output"
    
    def input_handler(self):
        input("Press Enter to stooutputp recording...\n")
        self.is_recording = False
    def record_video_segment(self, local_server_ip, save_directory, video_filename = 'output', is_full_video=False,is_train=False, label = None):
        # Determine the filename
        local_server_ip = self.local_server_ip
        save_directory= self.save_directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if is_full_video:
            
            filename = f'{save_directory}{video_filename}_{timestamp}.mp4'
        elif is_train:
            filename = f'{save_directory}{video_filename}_{timestamp}_{label}.mp4'
        else:
            filename = f'{save_directory}/outputs/{video_filename}.mp4'

        try:
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_video = cv2.VideoWriter(filename, fourcc, 60.0, (640, 480))

            # Capture video from the local server
            cap = cv2.VideoCapture(local_server_ip)

            if not cap.isOpened():
                print("Error: Could not open video stream from local server")
                return None

            # Record for 2 seconds
            counter = 0
            while self.is_recording:
                ret, frame = cap.read()
                if ret:
                    out_video.write(frame)
                    counter =counter +1
                if counter == 256:
                    break

            return filename
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            # Ensure resources are released
            cap.release()
            out_video.release()
    def record_video_net(self):
        input_thread = threading.Thread(target=self.input_handler)
        input_thread.start()
        classes =  self.classes
        save_directory = self.save_directory
        save_directory_full_vids = self.save_directory_full_vids
        save_directory_good_vids = self.save_good_vids_directory
        while self.is_recording:

                    # Save segment with constant filename (overwriting)
            _ = self.record_video_segment(self.local_server_ip, save_directory, self.video_filename, is_full_video=False)
                    # Save full video with unique filename

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            segment__ = os.path.join(save_directory_full_vids, f'{self.video_filename}_{timestamp}.mp4')
            shutil.copy(_, segment__)

            clas, prob = self.infer()
            if not _:
                print("Error recording video segment, trying again...")
            print(prob)
            if prob > 0.5:
                #saving for dataset 
                good__ = os.path.join(save_directory_good_vids, f'{self.video_filename}_{clas}_{timestamp}.mp4')
                shutil.copy(_, good__)
    
    def sample_frame_indices(self, vr, start_time, stop_time):
        assert start_time < stop_time
        total_frames = len(vr)

        start_idx = int(start_time * vr.get_avg_fps())
        stop_idx = int(stop_time * vr.get_avg_fps())
        
        start_idx = max(start_idx, 0)
        stop_idx = min(stop_idx, total_frames-1)
        assert start_idx < stop_idx
        
        skip = (stop_idx - start_idx) / 31
        indices = np.arange(start_idx, stop_idx+1, skip, dtype=np.int64)[:32]
        return indices
    def infer_activity(self, start_time=0, stop_time=16):
    # Open video and sample frames
        videoreader = VideoReader(self.video_path, num_threads=1)
        indices = self.sample_frame_indices(videoreader, start_time, stop_time)
        video = videoreader.get_batch(indices).asnumpy()
        # Prepare inputs
        inputs = self.processor(text=self.classes, videos=list(video), return_tensors="pt", padding=True)
        inputs = inputs.to(self.device)
        
        # Model inference
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Softmax to get probabilities
        probs = outputs.logits_per_video.softmax(dim=1)
        
        # Get the max probability and its index, excluding the last class initially
        prob_not_last = probs[:, :-1]
        max_prob_not_last, index_not_last = torch.max(prob_not_last, dim=1)
        
        # Threshold check against 'no human activity detected'
        if max_prob_not_last.item() < 0.1 + probs[:, -1].item():
            index = len(self.classes) - 1  # Index for 'no human activity detected'
        else:
            index = index_not_last.item()
        print (probs)
        # Result output
        if index == len(self.classes) - 1:
            print("None of the assigned activities is detected.")
        else:
            print(f"Detected activity: {self.classes[index]}")
            
        return self.classes[index],  max_prob_not_last.item()
    def infer(self):

        classes = self.classes
        activity, prob = self.infer_activity()
        return activity, prob
    
if __name__ == "__main__":
    labeler = AutoLabeler()
    labeler.record_video_net()