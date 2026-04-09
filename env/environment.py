import random
from env.tasks import TASKS
from env.grader import Grader


class DataCleaningEnv:
    def __init__(self):
        self.tasks = TASKS
        self.current_task = None
        self.grader = Grader()

    def reset(self):
        self.current_task = random.choice(self.tasks)
        return {
            "dataset": self.current_task["input"]
        }

    def step(self, action):
        if self.current_task is None:
            self.reset()

        cleaned_data = action.get("cleaned_data", [])
        expected = self.current_task["output"]
        reward = self.grader.grade(cleaned_data, expected)

        return {
            "observation": {
                "dataset": cleaned_data
            },
            "reward": reward,
            "done": True,
            "info": {}
        }
