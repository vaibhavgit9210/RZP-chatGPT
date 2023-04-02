import openai
import PySimpleGUI as sg
import requests
import webbrowser
import re

with open('openai_api_key.txt', 'r') as file:
    api_key = file.read().strip()

openai.api_key = api_key

my_theme = {
    "BACKGROUND": "#0D94FB",
    "TEXT": "#ffffff",
    "INPUT": "#012652",
    "TEXT_INPUT": "#E5E4E2",
    "SCROLL": "#c7e78b",
    "BUTTON": ("#000080", "#ffffff"),
    "PROGRESS": ("#01826B", "#D0D0D0"),
    "BORDER": 1,
    "SLIDER_DEPTH": 0,
    "PROGRESS_DEPTH": 0
}

# Set custom theme
sg.theme_add_new("MyTheme", my_theme)
sg.theme("MyTheme")


messages = [
    {"role": "system", "content": "You are a helpful and kind AI Assistant."},
]

layout = [
    [sg.Text("Chat with AI", font=("Arial", 12))],
    [sg.Multiline(key="-INPUT-", size=(100, 10),font=("Arial", 12))],
    [sg.Button("Ask",button_color=('black', 'lightgreen')),sg.Button("Save", button_color=('black', 'orange')), sg.Button("Leave", button_color=('black', 'red')), sg.Button("Clear", button_color=('black', 'grey'))],
    [sg.Output(size=(100, 40), key="-OUTPUT-",font=("Arial", 12))],
    [sg.Text("Powered by Razorpay - ChatGPT", font=("Arial", 12))]
    
]

window = sg.Window("LazyNinJa-Shuriken bot", layout)

def generate_image(prompt):
    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "response_format":"url",
        "size": "512x512"
    }

    response = requests.post(url, headers=headers, json=data)
    output = response.json()
    print (f"AI:  {response.json()}")
    url_key = output['data']
    url = url_key[0]['url']
    webbrowser.open(url)

    print("-------------------------------------x-------------------------------------------------")


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Leave":
        break
    elif event == "Ask":
        input_text = values["-INPUT-"]
        if input_text:
            messages.append({"role": "user", "content": input_text})
            prompt = input_text.replace("image of", "").strip()
            if "image of" in input_text:
                print(f"User:  {input_text}\n")
                print("-------------------------------------x-------------------------------------------------")
                generate_image(prompt)
            else:
                chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
                )
                reply = chat.choices[0].message.content
                messages.append({"role": "assistant", "content": reply})
                print(f"User:  {input_text}\n")
                print("-------------------------------------x-------------------------------------------------")
                print(f"\nAI: {reply}")
                match = re.search("(?P<url>https?://[^\s]+)", reply)
                if match:
                    url = match.group("url")
                    webbrowser.open(url)
                else:
                    print("No URL found in the text.")

            window["-INPUT-"].update("")
    elif event == "Save":
        filename = sg.popup_get_file(
            "Save chat log as:",
            save_as=True,
            file_types=(("DOCX Files", "*.docx"),),
            default_extension=".docx",
        )
        if filename:
            with open(filename, "w") as f:
                for message in messages:
                    f.write(f"{message['role']}: {message['content']}\n")
            sg.popup(f"Chat log saved to {filename}")
    elif event == "Clear":
        window["-OUTPUT-"].update("")
        
window.close()