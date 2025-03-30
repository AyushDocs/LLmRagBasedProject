from PIL import Image
import pandas as pd
import json
import requests
import subprocess
import time
import gzip
import re
from collections import defaultdict
import os

# Task 1: Calculate total margin for Theta sold in IN before a specific date
def total_margin_theta(data: dict):
    df = pd.read_excel(data['file_path'])
    df = df[(df['Product'].str.contains('Theta', case=False)) & (df['Country'].str.contains('IN', case=False))]
    df = df[df['Transaction Date'] < pd.to_datetime(data['before_date'])]
    return df['Margin'].sum()

# Task 2: Count unique student IDs from a text file
def count_unique_students(data: dict):
    with open(data['file_path'], 'r') as file:
        student_ids = set()
        for line in file:
            line = line.strip()
            if line:
                match = re.search(r'-(\d{10})', line.replace(" ", ""))
                if match:
                    student_ids.add(match.group(1))
    return len(student_ids)

# Task 3: Count successful GET requests under /malayalam/ on Wednesdays 0-6 AM
def count_successful_malayalam_requests(data: dict):
    count = 0
    with gzip.open(data['file_path'], 'rt') as file:
        for line in file:
            match = re.search(r'\[(\d{2})/May/2024:(\d{2}):', line)
            if match and int(match.group(1)) % 7 == 3 and 0 <= int(match.group(2)) < 6:
                if 'GET /malayalam/' in line and re.search(r'\s(2\d{2})\s', line):
                    count += 1
    return count

# Task 4: Find top data consumer for /hindimp3/ on 2024-05-23
def top_hindimp3_consumer(data: dict):
    ip_data = defaultdict(int)
    with gzip.open(data['file_path'], 'rt') as file:
        for line in file:
            if 'GET /hindimp3/' in line and '[23/May/2024' in line:
                match = re.search(r'^(\S+)', line)
                size_match = re.search(r'\s(\d+)\s"', line)
                if match and size_match:
                    ip_data[match.group(1)] += int(size_match.group(1))
    return max(ip_data.items(), key=lambda x: x[1])

# Task 5: Calculate Pizza sales in Jakarta (min 85 units)
def pizza_sales_jakarta(data: dict):
    OPENREFINE_URL = "http://127.0.0.1:3333"
    DATA_FILE = data['file_path']
    PROJECT_NAME = "SalesData"

    """Starts OpenRefine as a subprocess."""
    process = subprocess.Popen(["./refine"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)  # Wait for OpenRefine to fully start

    """Uploads the dataset to OpenRefine and returns the project ID."""
    print("Uploading dataset to OpenRefine...")
    files = {'project-file': open(DATA_FILE, "rb")}
    data = {'project-name': PROJECT_NAME}
    
    response = requests.post(f"{OPENREFINE_URL}/command/core/create-project-from-upload", files=files, data=data)
    if response.status_code == 200:
        project_id = response.json()['projectID']
        print(f"Project created successfully! Project ID: {project_id}")
    else:
        print("Error creating project:", response.text)
        return None

    """Computes fuzzy clusters for the 'city' column in OpenRefine."""
    print("Computing fuzzy clusters for city names (manual review needed)...")
    cluster_url = f"{OPENREFINE_URL}/command/core/compute-cluster?project={project_id}&columnName=city"
    response = requests.post(cluster_url)

    if response.status_code == 200:
        print("Clusters computed! Please review them in OpenRefine before proceeding.")
    else:
        print("Error computing clusters:", response.text)

    """Filters sales data for Pizza with at least 85 units sold."""
    print("Applying filters: product='Pizza' and sales >= 85...")
    filter_query = {
        "engine": json.dumps({"facets": [
            {"type": "text", "name": "product", "columnName": "product", "expression": "value == 'Pizza'"},
            {"type": "range", "name": "sales", "columnName": "sales", "expression": "value", "from": 85}
        ]})
    }
    
    filter_url = f"{OPENREFINE_URL}/command/core/apply-operations?project={project_id}"
    response = requests.post(filter_url, data=filter_query)
    
    if response.status_code == 200:
        print("Filters applied successfully!")
    else:
        print("Error applying filters:", response.text)

    """Exports the cleaned data from OpenRefine."""
    print("Exporting cleaned data from OpenRefine...")
    export_url = f"{OPENREFINE_URL}/command/core/export-rows?project={project_id}&format=csv"
    response = requests.get(export_url)

    if response.status_code == 200:
        with open("cleaned_sales_data.csv", "wb") as f:
            f.write(response.content)
        print("Cleaned data exported successfully!")
    else:
        print("Error exporting data:", response.text)

    """Loads the cleaned data and calculates total sales in Jakarta."""
    print("Analyzing sales for Jakarta...")
    df = pd.read_csv("cleaned_sales_data.csv")
    
    jakarta_sales = df[df['city'] == 'Jakarta']['sales'].sum()
    print(f"Total Pizza units sold in Jakarta (≥ 85 per transaction): {jakarta_sales}")

    print("Stopping OpenRefine...")
    process.terminate()

    #################################

# Task 6: Sum total sales from JSON file
def total_sales(data: dict):
    sales=0
    with open(data['file_path'], 'r') as file:
        for line in file:
            sales+=int(line[line.index('"sales":'):line.index(',',line.index('"sales":'))])
    return sales

# Task 7: Count occurrences of key 'J' in JSON log file
def count_key_occurrences(data: dict):
    def recursive_count(d):
        count = 0
        if isinstance(d, dict):
            count += d.get('J', 0)
            for v in d.values():
                count += recursive_count(v)
        elif isinstance(d, list):
            for v in d:
                count += recursive_count(v)
        return count
    
    with open(data['file_path'], 'r') as file:
        log_data = json.load(file)
    return recursive_count(log_data)

# Task 8: Find posts with high-engagement comments using DuckDB
def find_high_engagement_posts(data: dict):
    return """SELECT post_id
        FROM social_media
        WHERE timestamp >= '2025-01-25T05:18:24.537Z'
        AND EXISTS ( SELECT 1
                    FROM json_each(comments) AS comment
                    WHERE json_extract_float(comment.value, '$.stars.useful') > 2) ORDER BY post_id ASC;"""
# Task 9: Transcribe a YouTube video segment
def transcribe_video_segment(data: dict):
    audio_file = data['file']
    WHISPER_URL = "https://aiproxy.sanand.workers.dev/openai/v1/audio/transcriptions"

    """Transcribes an audio file using OpenAI Whisper."""
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
    }
    
    files = {
        "file": (audio_file, open(audio_file, "rb"), "audio/wav"),
        "model": (None, "whisper-1")
    }
    
    response = requests.post(WHISPER_URL, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json().get("text")
    else:
        print("Error:", response.text)
        return None

# Task 10: Reconstruct scrambled image from mapping
def reconstruct_image(data: dict):
    image = Image.open(data['image_path'])
    piece_size = image.width // 5
    new_image = Image.new('RGB', (image.width, image.height))
    
    for mapping in data['mapping']:
        orig_r, orig_c, scram_r, scram_c = mapping
        box = (scram_c * piece_size, scram_r * piece_size, (scram_c+1) * piece_size, (scram_r+1) * piece_size)
        piece = image.crop(box)
        new_image.paste(piece, (orig_c * piece_size, orig_r * piece_size))
    
    output_path = "reconstructed.png"
    new_image.save(output_path)
    return output_path
