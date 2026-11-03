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
<img width="994" height="517" alt="Screenshot1" src="https://github.com/user-attachments/assets/4a781303-6d92-434d-b1a6-bee1add0be84" />
<img width="1002" height="518" alt="Screenshot2" src="https://github.com/user-attachments/assets/413ce2ed-c390-46de-b955-cb1048c83be7" />
<img width="877" height="519" alt="Screenshot3" src="https://github.com/user-attachments/assets/3fb263fc-16cb-4293-a91d-fe91ba948d84" />

## Author
Laiba Sarwar
