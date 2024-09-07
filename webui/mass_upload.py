import os
import json
import shutil
import sys

# Add the root directory of the project to the system path to allow importing modules from the project
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    print("******** sys.path ********")
    print(sys.path)
    print("")

from webui.upload_youtube import upload_youtube



# def get_file_paths(folder):
#     file_paths = []
# 
#     # Walk through the folder and its subfolders
#     for root, dirs, files in os.walk(folder):
#         # Check for both "final-1.mp4" and "script.json"
#         if 'final-1.mp4' in files and 'script.json' in files:
#             final_mp4_path = os.path.join(root, 'final-1.mp4')
#             script_json_path = os.path.join(root, 'script.json')
#             file_paths.append((os.path.abspath(final_mp4_path), os.path.abspath(script_json_path)))
# 
#     return file_paths

def get_file_paths(folder):
    file_paths = []

    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder):
        # Check for both "final-1.mp4" and "script.json"
        if 'final-1.mp4' in files and 'script.json' in files:
            final_mp4_path = os.path.join(root, 'final-1.mp4')
            script_json_path = os.path.join(root, 'script.json')
            file_paths.append((os.path.abspath(final_mp4_path), os.path.abspath(script_json_path), root))

    return file_paths

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Folder path
folder_path = r'D:\DEV\MoneyPrinterTurbo\storage\to_upload\january'
uploaded_folder_path = r'D:\DEV\MoneyPrinterTurbo\storage\to_upload\january_uploaded'

# Create the "january_uploaded" folder if it doesn't exist
if not os.path.exists(uploaded_folder_path):
    os.makedirs(uploaded_folder_path)

# Get the file paths
file_paths = get_file_paths(folder_path)

# Extract data from script.json files
for final_mp4, script_json, subfolder in file_paths:
    print(f'Processing script.json: {script_json}')
    
    # Read and parse the JSON file
    data = read_json_file(script_json)
    
    # Extract the desired fields
    script_text = data.get('script', 'No script found')
    video_subject = data['params'].get('video_subject', 'No video subject found')
    video_materials = data['params'].get('video_materials', [])

    author = script_text.split('.')[0].title()
    
    # Print the extracted data
    print(f'Script: {script_text}')
    print(f'Video Subject: {video_subject}')
    print(f'Author: {author}')
    print(final_mp4)



    upload_youtube(video_file=final_mp4, title=video_subject, description=script_text, tags=[author,])

    # After successful upload, move the subfolder to "january_uploaded"
    destination = os.path.join(uploaded_folder_path, os.path.basename(subfolder))
    print(f'Moving folder: {subfolder} to {destination}')
    shutil.move(subfolder, destination)
    print(f'Successfully moved {subfolder} to {destination}')