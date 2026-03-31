import random
from env.tasks import TASKS
from env.grader import grade

class DataCleaningEnv:

    def __init__(self):
        self.current_task = None

    def reset(self):
        self.current_task = random.choice(TASKS)
        return {
            "dataset": self.current_task["input"]
        }

    def step(self, action):
        pred = action.get("cleaned_data", [])
        gt = self.current_task["output"]

        score = grade(pred, gt)

        # penalties
        if not isinstance(pred, list):
            score -= 0.3

        for item in pred:
            if not all(k in item for k in ["name", "age", "email"]):
                score -= 0.2

        score = max(0, min(score, 1))

        return (
            {"dataset": self.current_task["input"]},
            score,
            True,
            {}
        )

    def state(self):
        return self.current_task