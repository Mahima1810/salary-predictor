# Salary Predictor (Linear Regression)

Beginner-friendly ML mini web app.

## What it does
- Inputs: Years of experience, Skills rating (1–10)
- Output: Estimated salary

## Project structure
```
/backend
  app.py
  model.pkl
/frontend
  index.html
  style.css
  script.js
requirements.txt
```

## Run locally
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
pip install -r ..\requirements.txt
python app.py
```

Then open: http://localhost:5000

## Deploy (Render)
- Create a new **Web Service** on Render
- Connect your GitHub repo
- Root directory: `ML_Models/Linear_regression/salary_predictor`
- Build command: `pip install -r requirements.txt`
- Start command: `python backend/app.py`

Render will give you a public URL after deploy.
