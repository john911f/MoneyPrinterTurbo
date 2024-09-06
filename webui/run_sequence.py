import os
import sys
import yaml
import shutil

# Add the root directory of the project to the system path to allow importing modules from the project
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    print("******** sys.path ********")
    print(sys.path)
    print("")

import os
import platform
from uuid import uuid4
from app.services import task as tm
from app.models.schema import MaterialInfo, VideoAspect, VideoConcatMode, VideoParams


def open_task_folder(task_id):
    try:
        sys = platform.system()
        path = os.path.join(root_dir, "storage", "tasks", task_id)
        if os.path.exists(path):
            if sys == "Windows":
                os.system(f"start {path}")
            if sys == "Darwin":
                os.system(f"open {path}")
    except Exception as e:
        print(e)







def process_yaml_files(source_folder, dest_folder):
    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)
    
    for filename in os.listdir(source_folder):
        if filename.endswith(".yaml"):
            file_path = os.path.join(source_folder, filename)
            
            # Read the YAML file
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
            
            # Create an instance of VideoParams with data from YAML
            params = VideoParams(
                video_subject=data.get('video_subject', ""),
                video_script=data.get('video_script', ""),
                video_terms=data.get('video_terms', ""),
                video_aspect=data.get('video_aspect', ""),
                video_concat_mode=data.get('video_concat_mode', ""),
                video_clip_duration=data.get('video_clip_duration', 0),
                video_count=data.get('video_count', 0),
                video_source=data.get('video_source', ""),
                video_materials=data.get('video_materials', []),
                video_language=data.get('video_language', ""),
                voice_name=data.get('voice_name', ""),
                voice_volume=data.get('voice_volume', 1.0),
                voice_rate=data.get('voice_rate', 0.8),
                bgm_type=data.get('bgm_type', ""),
                bgm_file=data.get('bgm_file', ""),
                bgm_volume=data.get('bgm_volume', 0.2),
                subtitle_enabled=data.get('subtitle_enabled', False),
                subtitle_position=data.get('subtitle_position', ""),
                custom_position=data.get('custom_position', 0.0),
                font_name=data.get('font_name', ""),
                text_fore_color=data.get('text_fore_color', "#000000"),
                text_background_color=data.get('text_background_color', "transparent"),
                font_size=data.get('font_size', 100),
                stroke_color=data.get('stroke_color', "#ffffff"),
                stroke_width=data.get('stroke_width', 1.5),
                n_threads=data.get('n_threads', 1),
                paragraph_number=data.get('paragraph_number', 1)
            )

            print(params)

            # task_id = str(uuid4())
            task_id = params.video_subject

            result = tm.start(task_id=task_id, params=params)
            # open_task_folder(task_id)
            
            # Move the file to the destination folder
            shutil.move(file_path, os.path.join(dest_folder, filename))

# Define source and destination folders
source_folder = 'webui/params'
dest_folder = 'webui/params_done'

# Process the YAML files
process_yaml_files(source_folder, dest_folder)

