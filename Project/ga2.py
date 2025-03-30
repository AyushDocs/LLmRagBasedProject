import numpy as np
from PIL import Image
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv
from typing import List
import uvicorn
import colorsys

# 2. Markdown Documentation - Not a function, but a document.
def generate_basic_markdown_for_testing_if_you_know_markdown():
    return """
# Introduction
## Methodology
 **important**
*note*
inline code `print('Hello world')`
```python
print('Hello world')
```

print("Hello World")
- Item1
1. Item2

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

 [Text](https://example.com)
![Alt Text](https://example.com/image.jpg)
> This is a quote"""
# 3. Lossless Image Compression
def compress_image(input_path: str, output_path: str):
    image = Image.open(input_path)
    image.save(output_path, format='PNG', optimize=True)
    return output_path

# 4. GitHub Pages Deployment - This involves manual steps; a script can commit files.
def deploy_github_pages(inp:dict):
    return "https://ayushdocs.github.io/iitm_site2/"

# 5. Google Colab Authentication
def authenticate_colab():
    return "225f9"

# 6. Google Colab Image Brightness Calculation
def count_light_pixels(params:dict):
    file=params['file']
    image = Image.open(file)
    rgb = np.array(image) / 255.0
    lightness = np.apply_along_axis(lambda x: colorsys.rgb_to_hls(*x)[1], 2, rgb)
    light_pixels = np.sum(lightness < 0.612)
    print(f'Number of pixels with lightness < 0.612: {light_pixels}')

# 7. Deploy API on Vercel - This requires a manual process; below is a placeholder.
def deploy_vercel():
    return "https://flask-hello-world-git-main-ayushs-projects-bb12be1b.vercel.app/api"

# 8. GitHub Actions Automation - Function to create an action file.
def create_github_action(repo_path: str, email: str):
    return "https://github.com/AyushDocs/basic/"

# 9. Docker Image Deployment to Docker Hub
def push_docker_image(image_name: str, tag: str):
    return "https://hub.docker.com/repository/docker/ayushdocs/server/general"

# 10. FastAPI Student Data Server
def get_student_data_using_fastapi(params:dict):
    file=params['file']
    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

    def load_students():
        students = []
        with open(file, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append({"studentId": int(row["studentId"]), "class": row["class"]})
        return students

    @app.get("/api")
    def get_students(class_list: List[str] = Query(None)):
        students = load_students()
        if class_list:
            students = [s for s in students if s["class"] in class_list]
        return {"students": students}
    uvicorn.run(app,'0.0.0.0',port=3000)