import gradio as gr
import requests
import json


def get_completion(prompt):
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt, "history": []}
    try:
        response = requests.post(
            url="http://127.0.0.1:6006", headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
        print(response.json())  # 打印返回的完整 JSON
        return response.json().get("response", "No response field found.")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")  # 打印错误信息
        return f"Error: {e}"


def chat_interface(prompt):
    response = get_completion(prompt)
    return response


if __name__ == "__main__":
    iface = gr.Interface(
        fn=chat_interface,
        inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
        outputs="text",
        title="Chat Interface with API",
        description="Enter a prompt and get response from your API",
        allow_flagging="never",
    )
    iface.launch(share=True)
