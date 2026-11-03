# CodeAlpha_TranslationTool

A simple language translation web app built for the **CodeAlpha AI Internship (Task 1)**.

## Features
- Enter text and choose source and target language
- Auto-detect source language
- Translation using Google Translate (via `deep-translator`)
- Copy button (built into the result box)
- Text-to-Speech to listen to the translation (`gTTS`)

## Tech Stack
Python, Streamlit, deep-translator, gTTS

## How to Run
```bash
git clone https://github.com/<your-username>/CodeAlpha_TranslationTool.git
cd CodeAlpha_TranslationTool
pip install -r requirements.txt
streamlit run app.py
```

## How It Works
1. User types text and picks languages.
2. The text is sent to Google Translate through `deep-translator`.
3. The translated text is shown on screen.
4. gTTS converts the translated text into audio.

## Screenshot
_Add a screenshot of your app here._

## Author
Laiba Sarwar
