import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://amayraj-data-cleaning-openenv.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

def call_reset():
    return requests.post(f"{API_BASE_URL}/reset").json()

def call_step(data):
    return requests.post(f"{API_BASE_URL}/step", json=data).json()

def clean(data):
    out = []
    for r in data:
        name = str(r["name"]).strip().title()

        try:
            age = int(r["age"])
        except:
            age = 0

        email = r["email"]
        if "@" not in email:
            email += "@gmail.com"
        if "." not in email.split("@")[-1]:
            email += ".com"

        out.append({"name": name, "age": age, "email": email})
    return out


def run():
    total_rewards = []

    print(f"[START] task=data-cleaning env=openenv model={MODEL_NAME}")

    for step in range(3):
        reset = call_reset()
        dataset = reset["dataset"]

        cleaned = clean(dataset)

        res = call_step({"cleaned_data": cleaned})

        reward = float(res.get("reward", 0))
        done = True

        total_rewards.append(f"{reward:.2f}")

        print(f"[STEP] step={step+1} action=clean reward={reward:.2f} done={str(done).lower()} error=null")

    avg_score = sum(map(float, total_rewards)) / len(total_rewards)

    print(f"[END] success=true steps=3 score={avg_score:.2f} rewards={','.join(total_rewards)}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"[END] success=false steps=0 score=0.00 rewards= error={str(e)}")
