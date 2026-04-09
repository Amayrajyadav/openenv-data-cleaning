from fastapi import FastAPI
from env.environment import DataCleaningEnv
from env.grader import Grader
import uvicorn

app = FastAPI()
env = DataCleaningEnv()
grader = Grader()


# ✅ REQUIRED: Health check
@app.get("/health")
def health():
    return {"status": "healthy", "service": "data-cleaning-env"}


# ✅ REQUIRED: Tasks listing — this is what the validator calls to find graders
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": [
            {
                "task_id": "easy",
                "name": "Easy Data Cleaning",
                "description": "Fix capitalization and basic formatting",
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
                "description": "Fix complex formatting, word-form ages, broken emails",
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


# ✅ REQUIRED: Grader endpoint — validator calls this to test scores
@app.post("/grader")
def grade(payload: dict):
    task_id = payload.get("task_id", "easy")
    cleaned_data = payload.get("cleaned_data", [])

    # Find the task by name
    task = None
    for t in env.tasks:
        if t["name"] == task_id:
            task = t
            break

    if task is None:
        return {"reward": 0.15, "error": f"Unknown task_id: {task_id}"}

    expected = task["output"]
    reward = grader.grade(cleaned_data, expected)
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
