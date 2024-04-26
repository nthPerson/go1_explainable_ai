#!/usr/bin/env python3

import cv2
import numpy as np
import torch
from datetime import datetime
from pathlib import Path
from decord import VideoReader
from transformers import XCLIPProcessor, XCLIPModel

class AutoLabeler:
    def __init__(self, model_name, local_server_ip):
        self.base_directory = Path(__file__).resolve().parent
        self.model = self.load_model(model_name)
        self.local_server_ip = local_server_ip

    def load_model(self, model_name):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        processor = XCLIPProcessor.from_pretrained(model_name)
        model = XCLIPModel.from_pretrained(model_name).to(device)
        return (model, processor, device)

    def setup_video_capture(self):
        """ Setup video capture from the local server. """
        cap = cv2.VideoCapture(self.local_server_ip)
        if not cap.isOpened():
            print("Error: Could not open video stream")
            return None
        return cap

    def setup_video_writer(self, cap):
        """ Prepare the file and video writer. """
        filename = self.base_directory / "output" / f"output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_video = cv2.VideoWriter(str(filename), fourcc, 20.0, (640, 480))
        return out_video, filename

    def record_loop(self, cap, out_video):
        """ Capture frames from the video stream and write them to the file. """
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out_video.write(frame)
            if cv2.waitKey(1) == ord('q'):
                break

    def cleanup(self, cap, out_video):
        """ Release resources and close the files. """
        cap.release()
        out_video.release()

    def record_video(self):
        cap = self.setup_video_capture()
        if cap is None:
            return None

        out_video, filename = self.setup_video_writer(cap)
        self.record_loop(cap, out_video)
        self.cleanup(cap, out_video)
        return filename
    
    def classify_activity(self, video_path, model, processor, device):
        videoreader = VideoReader(video_path, num_threads=1)
        indices = np.linspace(0, len(videoreader) - 1, num=32, dtype=int)
        frames = videoreader.get_batch(indices).asnumpy()

        inputs = processor(text=["human is hammering", "human is measuring", "human is stacking boxes", 
                                 "human is scissoring", "human is cutting", "human is drilling", "no human in scene"], 
                           videos=list(frames), return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            logits = model(**inputs).logits_per_video.softmax(dim=1)

        best_prob, best_idx = torch.max(logits, dim=1)
        return processor.tokenizer.decode(best_idx), best_prob.item()

    def monitor_video_stream(self):
        video_path = self.record_video()
        if video_path:
            activity, probability = self.classify_activity(video_path, *self.model)
            print(f"Activity: {activity}, Probability: {probability}")

if __name__ == "__main__":
    local_server_ip = "http://146.244.98.19:5000/video_feed"
    model_name = "microsoft/xclip-base-patch16-zero-shot"
    labeler = AutoLabeler(model_name, local_server_ip)
    labeler.monitor_video_stream()
