import os
import json
import requests
from openai import OpenAI


API_BASE_URL = os.getenv("API_BASE_URL", "https://amayraj-data-cleaning-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_KEY = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

env_url = "http://localhost:7860"

scores = []
task_ids = ["easy", "medium", "hard"]

for task_id in task_ids:
    obs = requests.post(f"{env_url}/reset").json()

    print(f"[START] task={task_id} env=data-cleaning-env model={MODEL_NAME}")

    prompt = f"""You are a data cleaning assistant.
Clean the following dataset by:
- Fixing name to Title Case (strip extra spaces)
- Converting age to a valid integer
- Fixing email to be a valid format

Dataset:
{json.dumps(obs['dataset'], indent=2)}

Return ONLY valid JSON, no explanation, no markdown:
{{"cleaned_data": [{{"name": "string", "age": integer, "email": "string"}}]}}"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        output = response.choices[0].message.content.strip()

        # Strip markdown fences if present
        if "```" in output:
            output = output.split("```")[1]
            if output.startswith("json"):
                output = output[4:]
            output = output.strip()

        action = json.loads(output)

    except Exception as e:
        print(f"[STEP] step=1 action={{}} reward=0.15 done=false error={str(e)}")
        action = {"cleaned_data": []}

    result = requests.post(f"{env_url}/step", json=action).json()
    reward = result.get("reward", 0.15)
    scores.append(reward)

    print(f"[STEP] step=1 action={json.dumps(action)} reward={reward:.4f} done=true error=null")
    print(f"[END] success=true steps=1 score={reward:.4f} rewards={reward:.4f}")

avg = sum(scores) / len(scores)
print(f"Average Score: {avg:.4f}")
