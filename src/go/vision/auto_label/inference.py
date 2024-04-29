#!/usr/bin/env python3
import torch
import numpy as np
import os
from decord import VideoReader
import shutil
# import torch # This is insane if torch is imported here it doesn't work

class Inferencer:
    def __init__(self, label_context, dir_context):
        self.label_context = label_context
        self.dir_context = dir_context
        self.classes = [
            'human is hammering',
            'human is measuring',
            'human is stacking boxes',
            'human is scissoring',
            'human is cutting',
            'human is drilling',
            'no human in scene'
        ]

    def infer_activity(self, video_path, start_time=0, stop_time=16):
        try:
            inputs = self.analyze_video(video_path, start_time, stop_time)
            probs = self.predict_activity_probabilities(inputs)
            activity, prob = self.determine_activity(probs)
        except:
            print("Skipping inferral after user quit")
            exit()
        if activity == "no human in scene":
            print("None of the assigned activities is detected.")
        else:
            print(f"Detected activity: {activity}")
        return activity, prob

    def predict_activity_probabilities(self, inputs):
        with torch.no_grad():
            outputs = self.label_context.model(**inputs)
        probs = outputs.logits_per_video.softmax(dim=1)
        return probs

    def determine_activity(self, probs):
        prob_not_last = probs[:, :-1]
        max_prob_not_last, index_not_last = torch.max(prob_not_last, dim=1)
        
        threshold = 0.1 + probs[:, -1].item()
        if max_prob_not_last.item() < threshold:
            index = len(self.classes) - 1
        else:
            index = index_not_last.item()

        activity = self.classes[index]
        prob = max_prob_not_last.item() if index != len(self.classes) - 1 else probs[:, -1].item()
        return activity, prob

    def analyze_video(self, video_path, start_time=0, stop_time=16):
        videoreader = VideoReader(video_path, num_threads=1)
        indices = self.sample_frame_indices(videoreader, start_time, stop_time)
        video = videoreader.get_batch(indices).asnumpy()
        inputs = self.label_context.processor(text=self.classes, videos=list(video), return_tensors="pt", padding=True)
        return inputs.to(self.label_context.device)

    def sample_frame_indices(self, vr, start_time, stop_time):
        total_frames = len(vr)
        start_idx = int(start_time * vr.get_avg_fps())
        stop_idx = int(stop_time * vr.get_avg_fps())
        start_idx = max(start_idx, 0)
        stop_idx = min(stop_idx, total_frames-1)
        skip = (stop_idx - start_idx) / 31
        indices = np.arange(start_idx, stop_idx+1, skip, dtype=np.int64)[:32]
        return indices

    def evaluate_and_save(self, video_file_path, timestamp):
        clas, prob = self.infer_activity(video_file_path)
        print(prob)
        if prob > 0.5:
            good_path = os.path.join(self.dir_context.good_vids_dir, f"{clas}_{timestamp}.mp4")
            shutil.copy(video_file_path, good_path)