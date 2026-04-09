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
    if env.current_task is None:
        env.reset()
    return env.step(action)


@app.get("/state")
def state():
    return {
        "task": env.current_task["name"] if env.current_task else None,
        "dataset": env.current_task["input"] if env.current_task else None
    }


def main():
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
