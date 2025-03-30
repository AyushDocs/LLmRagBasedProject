import requests
import re
import pdfplumber
from bs4 import BeautifulSoup

# 1. ESPN Cricinfo - Count Ducks on Page 21
def count_ducks_espn():
    url = "https://stats.espncricinfo.com/ci/engine/stats/index.html?page=21"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ducks = sum(int(td.text) for td in soup.find_all("td", text=re.compile("^\d+$")))
    return {"total_ducks": ducks}
count_ducks_espn()
# 2. IMDb - Fetch Movies with Rating Between 4 and 5
def fetch_imdb_movies():
    url = "https://www.imdb.com/search/title/?user_rating=4.0,5.0"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    movies = []
    for movie in soup.find_all("div", class_="lister-item")[:25]:
        title = movie.h3.a.text
        year = movie.find("span", class_="lister-item-year").text
        rating = movie.find("strong").text if movie.find("strong") else "N/A"
        movie_id = re.search(r"tt\d+", movie.h3.a["href"]).group()
        movies.append({"id": movie_id, "title": title, "year": year, "rating": rating})
    return movies

# 3. Wikipedia - Extract Headings for a Country
def fetch_wikipedia_outline(country):
    url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    headings = [tag.text.strip() for tag in soup.find_all(re.compile("^h[1-6]$"))]
    return {"country": country, "outline": headings}

# 4. BBC Weather - Get Forecast for San Francisco
def fetch_weather_san_francisco():
    api_url = "https://weather.api.bbc.com/fake-endpoint"
    params = {"city": "San Francisco", "api_key": "your_api_key"}
    response = requests.get(api_url, params=params)
    return response.json()

# 5. Nominatim API - Get Maximum Latitude of Cairo
def get_cairo_max_lat():
    url = "https://nominatim.openstreetmap.org/search"
    params = {"city": "Cairo", "country": "Egypt", "format": "json"}
    response = requests.get(url, params=params)
    data = response.json()[0]
    return {"max_latitude": data["boundingbox"][1]}

# 6. Hacker News - Find Latest Post About Signal
def find_hn_post_signal():
    url = "https://hnrss.org/newest"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "xml")
    for item in soup.find_all("item"):
        if "Signal" in item.title.text and int(item.find("score").text) >= 36:
            return {"link": item.link.text}
    return None

# 7. GitHub API - Find Newest User in Tokyo with 130+ Followers
def find_newest_github_user_tokyo():
    url = "https://api.github.com/search/users"
    params = {"q": "location:Tokyo followers:>130", "sort": "joined", "order": "desc"}
    headers = {"Authorization": "Bearer your_github_token"}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()["items"][0]
    return {"username": data["login"], "created_at": data["created_at"]}

# 8. GitHub Actions - Create a Daily Commit Workflow
def create_github_action():
    workflow_yaml = """
    name: Daily Commit
    on:
      schedule:
        - cron: '0 2 * * *'  # Runs at 2 AM UTC daily
    jobs:
      commit:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout repository
            uses: actions/checkout@v2
          - name: Commit Change
            run: |
              date > date.txt
              git add date.txt
              git commit -m "Automated commit"
              git push
    """
    return {"workflow": workflow_yaml}

# 9. Parse PDF for Student Marks
def parse_student_marks(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)
    total_biology_marks = sum(map(int, re.findall(r"\b(\d+)\b", text)))
    return {"total_biology_marks": total_biology_marks}

# 10. Convert PDF to Markdown
def pdf_to_markdown(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join(page.extract_text() for page in pdf.pages)
    markdown = text.replace("\n", "\n\n")
    return {"markdown_content": markdown}
