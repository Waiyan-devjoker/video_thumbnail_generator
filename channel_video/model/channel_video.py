from odoo import models, fields, api
import base64
import cv2
import tempfile
import os
from PIL import Image
from io import BytesIO

class ChannelVideo(models.Model):
    _name = 'channel.video'
    _description = 'Channel Video'

    name = fields.Char(string='Name')
    video_file = fields.Binary(string='Video File')
    video_file_name = fields.Char(string='Video File Name')
    video_thumbnail = fields.Binary(string='Video Thumbnail')
    video_file_size = fields.Char(string='Video File Size')
    video_duration = fields.Char(string='Video Duration')

    def action_generate_video_properties(self):
        for record in self:
            if not record.video_file:
                continue  # Skip if there's no video file

            # Decode the base64 video file and write to a temporary file
            video_data = base64.b64decode(record.video_file)

            # write to a temporary file custom location
            # temp_dir = '/'  # Change to your local temp directory
            # temp_video_path = os.path.join(temp_dir, f"{record.name}.mp4")  # Use a unique name
            # with open(temp_video_path, 'wb') as temp_video_file:
            #     temp_video_file.write(video_data)

            # write to a temporary file system location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
                temp_video_file.write(video_data)
                temp_video_path = temp_video_file.name

            # Open the video and extract properties
            cap = cv2.VideoCapture(temp_video_path)
            if not cap.isOpened():
                raise ValueError("Could not open the video file.")

            # Calculate duration, file size, and thumbnail
            fps = cap.get(cv2.CAP_PROP_FPS) or 1  # Avoid division by zero
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            duration = frame_count / fps
            record.video_duration = f"{int(duration // 60)}:{int(duration % 60):02d}"
            record.video_file_size = f"{round(os.path.getsize(temp_video_path) / (1024 * 1024), 2)} MB"

            # Generate thumbnail
            cap.set(cv2.CAP_PROP_POS_MSEC, 1000)  # Set to 1 second
            success, frame = cap.read()
            if success:
                img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                img = img.resize((700, int(700 * (img.height / img.width))), Image.LANCZOS)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                record.video_thumbnail = base64.b64encode(buffered.getvalue()).decode('utf-8')

            cap.release()
            os.remove(temp_video_path)