from fastapi import FastAPI
from env.environment import DataCleaningEnv
from env.grader import Grader
import uvicorn

app = FastAPI()
env = DataCleaningEnv()
grader = Grader()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "data-cleaning-env"}


@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "task_id": "easy",
                "name": "Easy Data Cleaning",
                "description": "Fix name capitalization and basic formatting",
                "difficulty": "easy",
                "has_grader": True
            },
            {
                "task_id": "medium",
                "name": "Medium Data Cleaning",
                "description": "Fix names, ages, and incomplete emails",
                "difficulty": "medium",
                "has_grader": True
            },
            {
                "task_id": "hard",
                "name": "Hard Data Cleaning",
                "description": "Fix complex names, word-form ages, broken emails",
                "difficulty": "hard",
                "has_grader": True
            }
        ],
        "action_schema": {
            "cleaned_data": {
                "type": "array",
                "items": {
                    "name": "string",
                    "age": "int",
                    "email": "string"
                }
            }
        }
    }


@app.post("/grader")
def grade(payload: dict):
    task_id = payload.get("task_id", "easy")
    cleaned_data = payload.get("cleaned_data", [])

    task = None
    for t in env.tasks:
        if t["name"] == task_id:
            task = t
            break

    if task is None:
        return {"reward": 0.15, "task_id": task_id, "error": f"Unknown task: {task_id}"}

    reward = grader.grade(cleaned_data, task["output"])
    return {"reward": reward, "task_id": task_id}


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
