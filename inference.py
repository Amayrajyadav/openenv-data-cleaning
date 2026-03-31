import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

env_url = "http://localhost:8000"

scores = []

for i in range(3):
    obs = requests.post(f"{env_url}/reset").json()

    prompt = f"""
    Clean this dataset:
    {obs['dataset']}

    Return JSON:
    {{"cleaned_data": [...]}}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        output = response.choices[0].message.content
        action = eval(output)

    except:
        action = {"cleaned_data": []}

    result = requests.post(f"{env_url}/step", json=action).json()
    print("Score:", result["reward"])
    scores.append(result["reward"])

print("Average:", sum(scores)/len(scores))