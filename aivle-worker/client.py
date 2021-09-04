import json


def get_submission():
    with open("/home/leo/aivle-runner-v2/submission.json", "r") as f:
        return json.loads(f.read())
