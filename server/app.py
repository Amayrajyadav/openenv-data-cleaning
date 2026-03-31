from fastapi import FastAPI
from env.environment import DataCleaningEnv
import uvicorn

app = FastAPI()
env = DataCleaningEnv()

@app.post("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: dict):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

# ✅ REQUIRED for OpenEnv
def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

# ✅ REQUIRED ENTRYPOINT
if __name__ == "__main__":
    main()