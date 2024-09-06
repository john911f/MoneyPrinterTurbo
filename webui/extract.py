import os
import yaml
import sys
import re
from bs4 import BeautifulSoup
import platform


# Add the root directory of the project to the system path to allow importing modules from the project
root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
if root_dir not in sys.path:
    sys.path.append(root_dir)
    print("******** sys.path ********")
    print(sys.path)
    print("")

from app.models.schema import VideoParams
from app.services import task as tm
from webui.upload_youtube import upload_youtube


file_path = '.\\webui\\process_book\\book.html'  # Replace with your HTML file path
base_yaml_path = '.\\webui\\base.yaml'  # Replace with your HTML file path

def get_last_line_without_comma(s):
    # Split the string into lines
    lines = s.strip().split('\n')
    # Get the last line
    last_line = lines[-1]
    # Remove trailing comma and space
    last_line = last_line.lstrip(', ').strip()
    return last_line


def extract_quote_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    extracted_details = []
    
    for quote in quotes:
        # Extract quote text
        quote_text_raw = quote.get_text(separator='\n', strip=True)

        pattern = r'“(.*?)”'
        quote_text = re.findall(pattern, quote_text_raw)


        chapter = get_last_line_without_comma(quote_text_raw)

        
        # Find the author and bibliography if present
        author = None
        bibliography = None
        for p in quote.find_all('p'):
            if '—' in p.get_text():
                # This is usually where the author and bibliography are found
                parts = p.get_text().split('—')
                if len(parts) > 1:
                    author = parts[1].split(',')[0].strip()
                    bibliography = parts[1].split(',')[1].strip() if ',' in parts[1] else None
        
        if len(quote_text) > 0:
            extracted_details.append({
                'quote': f'{author.upper()}. {bibliography.upper()} {chapter}. \n{quote_text[0]}',
                'author': author.title(),
                'bibliography': f'{author.title()}, {bibliography.title()}, {chapter}'
            })
    
    return extracted_details

def read_html_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_video(video_subject=None, video_script=None):
    # Read the YAML file
    with open(base_yaml_path, 'r') as file:
        data = yaml.safe_load(file)

    if video_subject is None:
        video_subject=data.get('video_subject', ""),
    
    if video_script is None:
        video_script=data.get('video_script', ""),
            
    # Create an instance of VideoParams with data from YAML
    params = VideoParams(
        video_subject=video_subject,
        video_script=video_script,
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
    video_output_path =result['videos'][0]

    print(f"Final Video Paths = {result['videos'][0]}")

    return video_output_path

    


# Example usage:
html_content = read_html_from_file(file_path)
quote_details = extract_quote_details(html_content)

for detail in quote_details:

    video_subject = detail['bibliography'].replace(',','')
    video_script = detail['quote']
    
    youtube_description = f"{detail['bibliography']}\n{detail['quote']}"
    youtube_tags = [detail['author'],]

    print('-------------------------------------------')
    print(youtube_description)
    print(youtube_tags)
    print('-------------------------------------------')

    video_output_path = generate_video(video_subject=video_subject, video_script=video_script)
    # upload_youtube(video_file=video_output_path, title=video_subject, description=youtube_description, tags=youtube_tags)
