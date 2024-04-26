import cv2
import numpy as np
import os
import shutil
import threading
import torch
from datetime import datetime
from decord import VideoReader
from transformers import XCLIPProcessor, XCLIPModel

class AutoLabelContext:
    def __init__(self, model_name="microsoft/xclip-base-patch16-zero-shot"):
        self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        self.processor = XCLIPProcessor.from_pretrained(model_name)
        self.model = XCLIPModel.from_pretrained(model_name).to(self.device)

class DirectoryContext:
    def __init__(self, base_dir: str = os.path.dirname(os.path.realpath(__file__))):
        self.save_dir = base_dir
        self.outputs_dir = os.path.join(base_dir, "outputs")
        self.full_vids_dir = os.path.join(base_dir, "full_vids")
        self.good_vids_dir = os.path.join(base_dir, "good_vids")
        self.output_video_path = os.path.join(self.outputs_dir, "output.mp4")
        self.video_filename = "output"
        self.create_dirs()

    def create_dirs(self):
        """ Ensure all necessary directories are created. """
        os.makedirs(self.outputs_dir, exist_ok=True)
        os.makedirs(self.full_vids_dir, exist_ok=True)
        os.makedirs(self.good_vids_dir, exist_ok=True)

def get_activities():
    """ Return a list of predefined activities. """
    return [
        'human is hammering',
        'human is measuring',
        'human is stacking boxes',
        'human is scissoring',
        'human is cutting',
        'human is drilling',
        'no human in scene'
    ]

class AutoLabeler():
    """ 
        Gets video stream from server and analyzes the activity being performed 
    """
    def __init__(self, local_server_ip: str = "http://146.244.98.19:5000/video_feed"):
        self.local_server_ip = local_server_ip
        self.dir_contxt = DirectoryContext()
        self.label_contxt = AutoLabelContext()
        self.is_recording = True
        
    def input_handler(self):
        STOP_RECORD_MSG = "Press Enter to stop recording...\n"
        input(STOP_RECORD_MSG)
        self.is_recording = False

    def record_video_segment(self, video_filename='output', is_full_video=False, is_train=False, label=None):
        """Record a video segment from a live video stream."""
        filename = self.construct_filename(video_filename, is_full_video, is_train, label)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(filename, fourcc, 60.0, (640, 480))
        cap = cv2.VideoCapture(self.local_server_ip)
        if not cap.isOpened():
            print("Error: Could not open video stream from local server")
            return None
        try:
            return self.capture_frames(cap, out_video, filename)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            cap.release()
            out_video.release()

    def construct_filename(self, video_filename, is_full_video, is_train, label):
        """Constructs the appropriate file path based on the video type."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if is_full_video:
            return os.path.join(self.dir_contxt.save_dir, f"{video_filename}_{timestamp}.mp4")
        elif is_train:
            return os.path.join(self.dir_contxt.save_dir, f"{video_filename}_{timestamp}_{label}.mp4")
        else:
            return os.path.join(self.dir_contxt.outputs_dir, f"{video_filename}.mp4")

    def capture_frames(self, cap, out_video:cv2.VideoWriter, filename, max_frames=256):
        """Captures frames from the video stream and writes them to the video file."""
        counter = 0
        while True:
            ret, frame = cap.read()
            if not ret or counter >= max_frames:
                break
            out_video.write(frame)
            counter += 1
        return filename

    def monitor_video_stream(self):
        input_thread = threading.Thread(target=self.input_handler)
        input_thread.start()
        try:
            while self.is_recording:
                self.process_video_segment()
        finally:
            input_thread.join()  # Ensure the input thread is cleaned up properly

    def process_video_segment(self):
        video_file_path = self.record_video_segment()
        if not video_file_path:
            print("Error recording video segment, trying again...")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.archive_video_segment(video_file_path, timestamp)
        self.evaluate_and_save(video_file_path, timestamp)

    def archive_video_segment(self, video_file_path, timestamp):
        archive_path = os.path.join(self.dir_contxt.full_vids_dir, f"{timestamp}.mp4")
        shutil.copy(video_file_path, archive_path)

    def evaluate_and_save(self, video_file_path, timestamp):
        clas, prob = self.infer_activity()
        print(prob)
        if prob > 0.5:
            good_path = os.path.join(self.dir_contxt.good_vids_dir, f"{clas}_{timestamp}.mp4")
            shutil.copy(video_file_path, good_path)
    
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
    

    def infer_activity(self, video_path, start_time=0, stop_time=16):
        inputs = self.analyze_video(video_path, start_time, stop_time)
        probs = self.predict_activity_probabilities(inputs)
        activity, prob = self.determine_activity(probs)
        if activity == "no human in scene":
            print("None of the assigned activities is detected.")
        else:
            print(f"Detected activity: {activity}")
        return activity, prob
    
    def predict_activity_probabilities(self, inputs):
        """Predicts probabilities for each activity class."""
        with torch.no_grad():
            outputs = self.model(**inputs)
        probs = outputs.logits_per_video.softmax(dim=1)
        return probs

    def determine_activity(self, probs):
        """Determines the most likely activity based on model probabilities."""
        prob_not_last = probs[:, :-1]
        max_prob_not_last, index_not_last = torch.max(prob_not_last, dim=1)
        
        threshold = 0.1 + probs[:, -1].item()  # Threshold based on 'no human in scene' class probability
        if max_prob_not_last.item() < threshold:
            index = len(self.classes) - 1  # Assume the last class is 'no human in scene'
        else:
            index = index_not_last.item()

        activity = self.classes[index]
        prob = max_prob_not_last.item() if index != len(self.classes) - 1 else probs[:, -1].item()
        return activity, prob
    
    def analyze_video(self, video_path, start_time=0, stop_time=16):
        videoreader = VideoReader(video_path, num_threads=1)
        indices = self.sample_frame_indices(videoreader, start_time, stop_time)
        video = videoreader.get_batch(indices).asnumpy()
        inputs = self.processor(text=self.classes, videos=list(video), return_tensors="pt", padding=True)
        return inputs.to(self.device)

if __name__ == "__main__":
    labeler = AutoLabeler()
    labeler.record_video_net()