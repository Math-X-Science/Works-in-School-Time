import requests
import json


def get_completion(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "history": []}
    response = requests.post(
        url="http://127.0.0.1:6006", headers=headers, data=json.dumps(data)
    )
    return response.json()["response"]


if __name__ == "__main__":
    import time

    start = time.time()
    print(
        get_completion(
            "两个月没来一次月经，但是来了20天不完。滴哒滴哒总有，做了b超，内莫厚1.5（女，44岁）"
        )
    )
    end = time.time()
    print(end - start)
