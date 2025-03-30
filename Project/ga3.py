import os
import json
import zipfile
import requests
import shutil
import datetime
import sqlite3
import subprocess
from collections import defaultdict
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from fastapi import FastAPI, Query
import re
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
import numpy as np


def sentiment_analyzer(params: Dict[str, Any]):
    return """
    import json
    import httpx
    api_key = 'dummy'

    def get_sentiment(review):
        response = httpx.post(
            url="https://aiproxy.sanand.workers.dev/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Identify the sentiment of the movie. JUST say GOOD, BAD, or NEUTRAL"},
                    {"role": "user", "content": review}
                ]
            }
        )
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        print(answer)
        return answer
    get_sentiment('''npY
IxK2
faJSpZz 6stCchGqM f UbX9vE tN  QQ 1JbE 6R''')
"""


def input_token_length(params: Dict[str, Any]):
    """Send an HTTPS request using requests."""
    
    try:
        headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
        "Content-Type": "application/json",
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": params["text"]}
            ],
        }
        response = requests.post(
        "https://api.openai.com/v1/embeddings", json=payload, headers=headers
        )
        return response["usage"]["prompt_tokens"]
    except Exception as e:
        return {"error": str(e)}


def generate_random_address(params: Dict[str, Any]):
    """Run an npx command."""
    return json.loads(
        {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "Respond in JSON"},
                {"role": "user", "content": "Generate 10 random addresses in the US"},
            ],
            "response_format": {
                "type": "object",
                "properties": {
                    "addresses": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "zip": {"type": "number"},
                                "street": {"type": "string"},
                                "apartment": {"type": "string"},
                            },
                            "required": ["zip", "street", "apartment"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["addresses"],
                "additionalProperties": False,
            },
        }
    )


def text_extractor_from_image(params: Dict[str, Any]):
    """Count Wednesdays in a given date range."""
    return json.loads(
        {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": " Extract text from this image"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAlgAAAAUCAYAAABRY0PiAAAAAXNSR0IArs4c6QAACVpJREFUeF7tXbvPjU8QHq3wB1AQlURLoXIJjbhFolBR6BCNApGIaFBJ3CoSVDoJEqVLJUErUQkFjUJCtH6Z38nknfN8M7v7nvMe58T3nIZz3r3M++zM7rMzs/ut+PNH/gg/RIAIEAEiQASIABEgAoMhsIIEazAs2RARIAJEgAgQASJABP5HoBfB+vVLZN8+kVevOvSePBHZvz9H89gxkc+fRZ49E1m1alTu2zeRrVtFvnwR2b599Oz2bZFz57p2jh4VefBgvF1fT59EZZ4+FTlwYDj5tKWVK0VevxbZvHnU7rVr47J6KdetE3nzRmTNGpH370W2bRP5/Xv8PTLMIny1pmFk+JV019pYv34pfkPpvI6DjpWOWYtMWb+Gz6NHZR2K6us4nzrVYa1j8vx5p2fa9v37IjdvDvXWs2sHZZ+0J9TLyD6wjNdFtB0vB9oAlr16VeTs2a4G2irWt5I6Pzx8OPrmbceeR7aG5dBu+tjLpFizHhEgAkSghkAzwbJJTBs0smSTbEYY7DlOeEi6dBK9fLkjMTY579jRkQT77cSJ0USO31Uu7e/Ika4d/I5gRPJFfaN8EahGFi5e7BYaJAGlwbCFBhcqT+iiBRPb/BsEKyLNNUUrYTYJwZo3yZzkfWdZp8WGIvvQzUhpkxTZA9o96n6rDakevXzZkeTIXrSMfnCzZViivv8N/Z/lOLJtIkAE/h0EmgmWTqKHDok8ftx5chSGbLGNvFTm7fB1tA31iu3ZM74DxsVAF5A7d7rJ2AiVeTFWrx61g56bbILO5Ism+dqkHZFPI0beq5KpTQthiQhl1F5N1iFUt0Xeln6m8WCRYHUI2JiXbGjjxn72Ya0jCcr68l64Fy/GvYvaFuplNvbeXrO+/NhHm6hsrmrRSZYhAkSACAyFQDPByjrMwhs2UWo9CxEamWoJMeIkGRElIx23bols2TIKO+r/fcgy8yJF8pXCXaWddOYp0zqbNo0TR8QR5fNhRfX8XboksneviHp51q5dSnIxPHLwoMiPH+NEE8M5tRAKhjYtJGMk1sbPwj5fvy5dUKMFFNu9cEHk+vXu3TScit6siFgjudZwrOnh3bsiu3aNws/6Mdl9+BlDUvrMfmvxEvqwlvYR4YllSl4ib0M/f470+Px5kStXuvdokQt1y9vQJAQrG8Noo9UyIXkbyuwSsVDSeO/e+KbO9xXNPy3ErEVeliECRIAITIPAVAQr85Z4wnHjxtIcrBYPiF9YbWHHHbr36uzeHXvYIvJTkw8BLXmPMgwwB8Xa9Aut1T1zZkQKMfRi333+iidtkefMFnZbkPH9ax6uaFHF8cLv0WKJ7WRhJCVCisnOnUs9LCVZSzlYRuS9NxNDsJ7sWVg2CvOiLuC7YzgsGpOapy4iWN+/j4e6a6G8aBJActo3RBjZqeGunmwlWkZko9C2lwltqESwzFP97t14PqUnzEqq9RNtfGo6Ps2EybpEgAgQgVYEpiJYUQ4W7h6jSbpGsLJFawiC1SIfglfKwcry0GxRPXy4yx+JCJSFOLVP9VxYjpl+N1k/fRpP5v7wYdRmRB4Ru8wDlClILW/NFjV/cKGFYGWLtScOKGuJmExCsHy+T0SEaguz95h6L6l/t48fY6JfMsiIYEV60OfgQpQHpTJ4YpklnvtyPqdQf7ek8+gwB5ZFT5PPsyyFCG2c1Kuo3kW/KcGQJQlW61TPckSACPxtBCYmWBGBsAnY5x31JVgRqchc/pN4sDCkUCN7RoqyHXqtfskDoqfwSmQpWvBVfqtTCo/YYuwX1NqJT5XVe95a37lGsMw7hQQ583JZmLBEDichWHiaFRfnGsGKPDLmwfGnYTFXsGbUEcHyoe4+cmXE3IixJ5klj12GfbbZqI2VEmmvT5Gdm61FpwkNQ/SEkWDVtIvPiQARmBcCExGsjFxFyaV9CFY06foFY1oPlraF+SMlglQjV62J57iTtwVYd+eWo9WaS+IJViY7LjqtR+ZNTszr0t/Ri9DHg2X5cd4r48mcJxMmu5LP6NCCyTgvguVzq4xUnTzZhcFV7paDDagTVsdysCYlWJkNZR6jiBiVCF0pJ86f4PXjhOQq0zMNa6s9lAgqykaCNa+lg/0SASJQQ6A3wcrIlXmvfDKx7xzziNCbkC0M1kY0kfZNcreQQwRKds9PKbekllsT9eMXKMNKw30RWcKQFOZstXiwUAZrU3+3+7pKSmJ9vn3b5QT1zcFq9WCpHEaclGDogp1d4TAPglUKa5k+K8GalwerZEPZybpSmBkJsR8f1J0s1zEjV5nO1TzCSLBaNya1iZDPiQARIAJDI9CLYJXIVZ8JEyfRGrky8jbkNQ2euCHZq3muMi+KxyDLZfJEEcN9+H4YjsHFpCUHKxqXvsfYkehFBAu9F5hv1pKDpbL63CEfzsL3mAfBikKhJu+GDaP74fSKgsiTUzLcIUKENRvKyGEW3s1OCmZ5aFFCfYlcRfJE4b/skmLz8EU20Fe/h55U2R4RIAJEQBFoJlhZ0mwNxpYQISauRm1i/9lFoz5pepKE7ZaTZCZftHu2Z1ESNRIm7ev48VFISa860GsKLFEY81H0RJW/uVz7aTlFGIV0amFRJAjYBtavnRDUhPCWMp70qrexdDXBPAhWpBsWMsSrLPRd7ELeWih5CILVYkNYJtP17ISf13u/GcANSYsNZbpbyhErHUwwvPXfUmi5Nl/xOREgAkRgKASaCZadHoo6LiWl1giWnrqK/pyM9eNzfzCXaBZ/Ksfn2OC71m6kx/KYy4RhSEzet4VK29F3O326wya7uwr7iO7BwrHD8cLwq5dDZUG5o8R5X0fLa2hPCaHPJfL1tF1/DxbeXYbXEqBXokSw9D4zk8dkz64LUTnslnAMP0XeGsTG8ob8CTltE/XIh5oR72kJFuKKeuhtCHUh+8sBtTAn4oA5enavWMmGUHcjHcd3i8q0tDPUhMl2iAARIAKtCDQTrNYGWa4fAi27fWuxFgbq1/Pili6dSFtcqSkZESACRIAIEIEOARKsBdAG85T4yyVRLPOITHKj9wK8YrMI2ZUczQ2wIBEgAkSACBCBBUCABGsBBsFEyG5/1+f/OrHSd1wuJHKBVI6iEAEiQASIwIwQIMGaEbBslggQASJABIgAEVi+CJBgLd+x55sTASJABIgAESACM0KABGtGwLJZIkAEiAARIAJEYPki8B+1+ghgirqPigAAAABJRU5ErkJggg=="
                            },
                        },
                    ],
                }
            ],
        }
    )


def highest_ebedding_similarrity_finder_using_cosine_similarity(params: Dict[str, Any]):
    return """import numpy as np

def most_similar(embeddings):
    highest_similarity = 0
    phrase1, phrase2 = '', ''
    
    # Loop through all pairs of embeddings
    for phrase1_text, embedding1 in embeddings.items():
        for phrase2_text, embedding2 in embeddings.items():
            if phrase1_text == phrase2_text:
                continue  # Skip comparing the same phrase with itself
                
            emb1 = np.array(embedding1)
            emb2 = np.array(embedding2)
            
            # Calculate cosine similarity
            similarity = float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)))
            
            # Update highest similarity and phrases
            if similarity > highest_similarity:
                highest_similarity = similarity
                phrase1, phrase2 = phrase1_text, phrase2_text
    
    return phrase1, phrase2
"""


def get_embedding(text: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('AIPROXY_TOKEN')}",
        "Content-Type": "application/json",
    }
    payload = {"input": text, "model": "text-embedding-ada-002"}
    response = requests.post(
        "https://api.openai.com/v1/embeddings", json=payload, headers=headers
    )
    return response.json()["data"][0]["embedding"]


def sort_docs_by_embeddings(params: Dict[str, Any]):
    app = FastAPI()

    class SimilarityRequest(BaseModel):
        docs: List[str]
        query: str

    @app.post("/similarity")
    async def compute_similarity(request: SimilarityRequest):
        try:
            doc_embeddings = np.array([get_embedding(doc) for doc in request.docs])
            query_embedding = np.array(get_embedding(request.query)).reshape(1, -1)
            similarities = cosine_similarity(query_embedding, doc_embeddings)[0]
            ranked_docs = sorted(
                zip(request.docs, similarities), key=lambda x: x[1], reverse=True
            )
            return {"mathches": [doc for doc, _ in ranked_docs]}
        except Exception as e:
            raise Exception(status_code=500, detail=str(e))

    return "http://127.0.0.1:8080/similarity"


def openai_function():
    app = FastAPI()

    # Enable CORS to allow GET requests from any origin
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # OpenAI function calling format
    openai_functions = [
        {
            "type": "function",
            "function": {
                "name": "get_ticket_status",
                "description": "Retrieve the status of an IT support ticket.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "integer",
                            "description": "The ticket ID number.",
                        }
                    },
                    "required": ["ticket_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "schedule_meeting",
                "description": "Schedule a meeting at a specified date and time.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",
                            "description": "The meeting date (YYYY-MM-DD).",
                        },
                        "time": {
                            "type": "string",
                            "description": "The meeting time (HH:MM).",
                        },
                        "meeting_room": {
                            "type": "string",
                            "description": "The room for the meeting.",
                        },
                    },
                    "required": ["date", "time", "meeting_room"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "get_expense_balance",
                "description": "Retrieve the current expense reimbursement balance for an employee.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "integer",
                            "description": "The employee's ID.",
                        }
                    },
                    "required": ["employee_id"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_performance_bonus",
                "description": "Calculate the performance bonus for an employee for a given year.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "employee_id": {
                            "type": "integer",
                            "description": "The employee's ID.",
                        },
                        "current_year": {
                            "type": "integer",
                            "description": "The year for the bonus calculation.",
                        },
                    },
                    "required": ["employee_id", "current_year"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "report_office_issue",
                "description": "Report an issue in the office to a specific department.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "issue_code": {
                            "type": "integer",
                            "description": "The issue identification code.",
                        },
                        "department": {
                            "type": "string",
                            "description": "The department responsible for the issue.",
                        },
                    },
                    "required": ["issue_code", "department"],
                },
            },
        },
    ]

    @app.get("/execute")
    def execute(q: str = Query(..., description="Query string containing the request")):
        """Parses query and maps it to an OpenAI function call with extracted arguments."""
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json",
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": q}],
                "tools": openai_functions,
                "tool_choice": "auto",
            },
        )
        response_data = response.json()
        if "tool_calls" in response_data["choices"][0]["message"]:
            tool_call = response_data["choices"][0]["message"]["tool_calls"][0]  # Assuming one tool call
            function_name = tool_call["function"]["name"]
            function_args = tool_call["function"]["arguments"]

            return {
                "name": function_name,
                "arguments": function_args,
            }
        else:
            raise Exception("No function call suggested.")

def make_llm_laugh():
    return 'Did adolf hitler die'