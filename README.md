# RZP-chatGPT

A 2023 experiment with the (then-new) OpenAI chat API, built during my time at Razorpay: a small desktop chat client ("LazyNinJa-Shuriken bot") written in Python with PySimpleGUI.

## What it does

`gpt3.py` opens a themed PySimpleGUI window with a text box, an output pane, and Ask / Save / Clear / Leave buttons:

- **Chat** — sends the conversation history to `gpt-3.5-turbo` via the `openai` library (0.27-era `ChatCompletion` API) and prints the reply. If the reply contains a URL, it's opened in the default browser.
- **Image generation** — if the prompt contains the phrase `"image of"`, it instead calls the DALL·E images endpoint (`/v1/images/generations`, 512x512) directly with `requests` and opens the resulting image URL in the browser.
- **Save** — dumps the chat transcript to a file (plain text, despite the `.docx` picker).

The API key is read from a local `openai_api_key.txt` file (not included — bring your own).

`My Movie.mp4` is a screen-recorded demo of the app in action.

## Contents

```
gpt3.py            # the whole app
requirement.txt    # pip freeze of the dev environment (much more than is needed)
My Movie.mp4       # demo video
```

## Running it

The only real dependencies are `openai==0.27.x`, `PySimpleGUI`, and `requests` (the code predates the openai v1 SDK, so newer versions won't work as-is):

```bash
pip install "openai==0.27.2" PySimpleGUI requests
echo "sk-..." > openai_api_key.txt
python gpt3.py
```
