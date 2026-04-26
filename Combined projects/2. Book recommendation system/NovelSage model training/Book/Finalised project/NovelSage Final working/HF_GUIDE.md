# NovelSage AI - Configuration Guide

To enable the AI Chatbot and secure the application, follow these steps:

## 1. Get Hugging Face API Token
1. Go to [Hugging Face Settings](https://huggingface.co/settings/tokens).
2. Click **"New token"**.
3. Name it (e.g., `NovelSage`) and set the role to **"Read"**.
4. Copy the generated token.

## 2. Setup Environment Variables
Create a file named `.env` in the `Final Project` folder and paste the following:

```env
SECRET_KEY=yoursecretkeyhere_any_long_string
HUGGINGFACE_API_TOKEN=your_token_from_step_1
```

## 3. Install Dependencies
Make sure you have the required libraries:
```bash
pip install flask flask-sqlalchemy flask-login huggingface_hub python-dotenv pandas numpy scipy scikit-learn
```

## 4. Run the App
```bash
python app.py
```
The database will be created automatically on the first run.
