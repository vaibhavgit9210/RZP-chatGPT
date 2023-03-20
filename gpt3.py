import openai
import PySimpleGUI as sg

openai.api_key = "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"

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
    [sg.Button("Ask"),sg.Button("Save"), sg.Button("Leave")],
    [sg.Output(size=(100, 40), key="-OUTPUT-",font=("Arial", 12))],
    [sg.Text("Powered by Razorpay - ChatGPT", font=("Arial", 12))]
    
]

window = sg.Window("LazyNinJa-Shuriken bot", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Leave":
        break
    elif event == "Ask":
        input_text = values["-INPUT-"]
        if input_text:
            messages.append({"role": "user", "content": input_text})
            chat = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=messages
            )
            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print(f"User: {input_text}")
            print(f"AI: {reply}")
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
window.close()