import os
import pandas as pd
import json
import zipfile
import requests
import shutil
import re
import hashlib
import datetime
import subprocess
from typing import  Dict, Any
from dateutil import parser


def make_http_request_with_uv(params: Dict[str, Any]):
    """Send an HTTPS request using requests."""
    try:
        url = params["url"]
        email = params["email"]
        response = subprocess.check_output(f'uv run --with httpie -- https {url}?email={email}'.split()).decode()
        response=response[response.index('{'):]
        return json.loads(response)
    except Exception as e:
        return {"error": str(e)}

def run_command_with_npx(params: Dict[str, Any]):
    """Run an npx command."""
    try:
        # TODO: make sure file path file is saved correctly
        command = params["command"]
        output = subprocess.check_output(["npx"] + command.split()).decode()
        return {"output": output}
    except Exception as e:
        return {"error": str(e)}

def count_wednesdays(params: Dict[str, Any]):
    """Count Wednesdays in a given date range."""
    try:

        start_date = params["start_date"]
        end_date = params["end_date"]
        start = parser.parse(start_date)
        end = parser.parse(end_date)
        count = sum(1 for d in range((end - start).days + 1) if (start + datetime.timedelta(days=d)).weekday() == 2)
        return {"wednesday_count": count}
    except Exception as e:
        return {"error": str(e)}

def extract_csv_from_zip(params: Dict[str, Any]):
    """Extract a CSV file from a ZIP and return values from a column."""
    try:
        zip_file_path = params["zip_file_path"]
        csv_file_name = params["csv_file_name"]
        column_name = params["column_name"]
        
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            with z.open(csv_file_name) as f:
                lines = f.read().decode().splitlines()
                headers = lines[0].split(",")
                column_index = headers.index(column_name)
                values = [line.split(",")[column_index] for line in lines[1:]]
                return {"values": values}
    except Exception as e:
        return {"error": str(e)}

def sort_json_array(params: Dict[str, Any]):
    """Sort a JSON array by specified fields."""
    try:
        json_array = params["json_array"]
        sort_fields = params["sort_fields"]
        return sorted(json_array, key=lambda x: tuple(x[field] for field in sort_fields))
    except Exception as e:
        return {"error": str(e)}

def process_files_with_encodings(params):
    """Process files with different encodings and sum specified values."""
    try:
        file_paths = params["file_paths"]
        encodings = params["encodings"]
        symbols = set(params["symbols"])  # Convert to a set for faster lookup
        total_sum = 0

        if len(file_paths) != len(encodings):
            return {"error": "Mismatch between number of file paths and encodings"}

        for file, encoding in zip(file_paths, encodings):
            delimiter = "\t" if file.endswith(".txt") else ","
            
            # Read the file with its specific encoding
            df = pd.read_csv(file, encoding=encoding, delimiter=delimiter)
            
            # Ensure column names are correct
            if "symbol" not in df.columns or "value" not in df.columns:
                return {"error": f"File {file} is missing required columns."}

            # Filter rows where the symbol is in the specified set
            df_filtered = df[df["symbol"].isin(symbols)]
            
            # Sum up the relevant values
            total_sum += df_filtered["value"].sum()

        return {"total_sum": total_sum}

    except Exception as e:
        return {"error": str(e)}
def download_and_process_zip(params):
    """Download a ZIP file, extract it, replace 'IITM' with 'IIT Madras', and compute the SHA256 checksum."""
    try:
        zip_url = params["zip_url"]
        destination_folder = params["destination_folder"]
        temp_zip_path = os.path.join(destination_folder, "temp.zip")

        # Step 1: Download the ZIP file
        import requests
        response = requests.get(zip_url, stream=True)
        if response.status_code != 200:
            return {"error": f"Failed to download file: {response.status_code}"}

        with open(temp_zip_path, "wb") as f:
            f.write(response.content)

        # Step 2: Extract ZIP contents
        extracted_folder = os.path.join(destination_folder, "unzipped")
        os.makedirs(extracted_folder, exist_ok=True)

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        os.remove(temp_zip_path)  # Cleanup zip file

        # Step 3: Replace 'IITM' in all files (case insensitive)
        pattern = re.compile(r"IITM", re.IGNORECASE)

        for root, _, files in os.walk(extracted_folder):
            for file in files:
                file_path = os.path.join(root, file)

                # Read file content without altering line endings
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.readlines()

                # Replace 'IITM' with 'IIT Madras' in a case-insensitive way
                modified_content = [pattern.sub("IIT Madras", line) for line in content]

                # Write back to the file
                with open(file_path, "w", encoding="utf-8", errors="ignore", newline="") as f:
                    f.writelines(modified_content)

        # Step 4: Compute SHA256 hash using 'cat * | sha256sum' equivalent
        sha256_hash = hashlib.sha256()
        for root, _, files in os.walk(extracted_folder):
            for file in sorted(files):  # Sort files to maintain consistent order
                file_path = os.path.join(root, file)
                with open(file_path, "rb") as f:
                    while chunk := f.read(4096):
                        sha256_hash.update(chunk)

        return {"sha256sum": sha256_hash.hexdigest()}

    except Exception as e:
        return {"error": str(e)}
def download_and_extract_zip(params):
    """Download a ZIP file, extract it while preserving timestamps, and list file details."""
    try:
        zip_url = params["zip_url"]
        destination_folder = params["destination_folder"]
        min_size = params["min_size"]
        min_timestamp = datetime.datetime.strptime(params["min_timestamp"], "%a, %d %b, %Y, %I:%M %p %Z")

        temp_zip_path = os.path.join(destination_folder, "temp.zip")

        # Step 1: Download the ZIP file
        response = requests.get(zip_url, stream=True)
        if response.status_code != 200:
            return {"error": f"Failed to download file: {response.status_code}"}

        with open(temp_zip_path, "wb") as f:
            f.write(response.content)

        # Step 2: Extract ZIP contents while preserving timestamps
        extracted_folder = os.path.join(destination_folder, "unzipped")
        os.makedirs(extracted_folder, exist_ok=True)

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted_folder)

        os.remove(temp_zip_path)  # Cleanup zip file

        # Step 3: List file details and calculate total size of matching files
        total_size = 0
        file_details = []

        for root, _, files in os.walk(extracted_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_stat = os.stat(file_path)

                # Get file modification time
                mod_time = datetime.datetime.fromtimestamp(file_stat.st_mtime)

                # Check conditions: size >= 7308 bytes and modified on or after given date
                if file_stat.st_size >= min_size and mod_time >= min_timestamp:
                    total_size += file_stat.st_size

                file_details.append({
                    "file": file,
                    "size": file_stat.st_size,
                    "modified": mod_time.strftime("%Y-%m-%d %I:%M %p")
                })

        return {
            "files": file_details,
            "total_size_matching_criteria": total_size
        }

    except Exception as e:
        return {"error": str(e)}

def download_extract_and_rename(params):
    """Download, extract, move, rename files, and simulate bash hash output."""
    try:
        zip_path = params["zip_path"]
        import uuid
        destination_folder = "./uploads/"+str(uuid.uuid4())
        final_folder = "./uploads/"+str(uuid.uuid4())

        os.makedirs(destination_folder)
        subprocess.run(f'unzip {zip_path} -d {destination_folder}', shell=True, check=True)

        os.removedirs(zip_path)
        os.removedirs(destination_folder)

        for root, _, files in os.walk(destination_folder):
            for file in files:
                original_path = os.path.join(root, file)
                new_path = os.path.join(final_folder, file)
                shutil.move(original_path, new_path)

        renamed_files = []
        for file in os.listdir(final_folder):
            new_name = re.sub(r"\d", lambda x: str((int(x.group(0)) + 1) % 10), file)
            old_path = os.path.join(final_folder, file)
            new_path = os.path.join(final_folder, new_name)
            os.rename(old_path, new_path)
            renamed_files.append(new_name)

        output=subprocess.check_output(f'cd {final_folder} && grep . * | LC_ALL=C sort | sha256sum ', shell=True, check=True)
        return output.decode().strip()[0]

    except Exception as e:
        return {"error": str(e)}
def compare_files(params: Dict[str, Any]):
    """Compare two files line by line."""
    try:
        file1_path = params["file1_path"]
        file2_path = params["file2_path"]
        with open(file1_path, 'r') as f1, open(file2_path, 'r') as f2:
            differences = sum(1 for line1, line2 in zip(f1, f2) if line1 != line2)
        return differences
    except Exception as e:
        return {"error": str(e)}

def calculate_ticket_sales(params: Dict[str, Any]):
    """Calculate ticket sales from a SQLite database."""
    return "SELECT SUM(units*price) FROM tickets WHERE TRIM(UPPER(type))='GOLD'"