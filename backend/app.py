import os
from typing import Any, Dict, Tuple

import joblib
import numpy as np
from flask import Flask, jsonify, request, send_from_directory
from sklearn.linear_model import LinearRegression


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")

_model: LinearRegression | None = None


def _train_and_save_dummy_model(model_path: str) -> None:
    rng = np.random.default_rng(42)

    # Dummy training data (beginner-friendly + deterministic)
    # Features: [years_experience, skills_rating]
    n = 400
    years = rng.uniform(0, 15, size=n)
    skills = rng.integers(1, 11, size=n)

    X = np.column_stack([years, skills]).astype(float)

    # Simple synthetic salary formula (+ small noise)
    noise = rng.normal(0, 2500, size=n)
    y = (30_000 + 6_000 * years + 4_000 * skills + noise).astype(float)

    model = LinearRegression()
    model.fit(X, y)

    joblib.dump(model, model_path)


def _load_model() -> LinearRegression:
    global _model

    if _model is not None:
        return _model

    if not os.path.exists(MODEL_PATH):
        _train_and_save_dummy_model(MODEL_PATH)

    _model = joblib.load(MODEL_PATH)
    return _model


def _parse_and_validate(payload: Dict[str, Any] | None) -> Tuple[np.ndarray, str | None]:
    if not isinstance(payload, dict):
        return np.empty((0, 2)), "Request body must be JSON."

    missing = [k for k in ("experience", "skills") if k not in payload]
    if missing:
        return np.empty((0, 2)), f"Missing fields: {', '.join(missing)}"

    try:
        experience = float(payload["experience"])
        skills = float(payload["skills"])
    except (TypeError, ValueError):
        return np.empty((0, 2)), "experience and skills must be numbers."

    if experience < 0:
        return np.empty((0, 2)), "experience must be 0 or greater."
    if skills < 1 or skills > 10:
        return np.empty((0, 2)), "skills must be between 1 and 10."

    X = np.array([[experience, skills]], dtype=float)
    return X, None


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True)
    X, error = _parse_and_validate(payload)
    if error:
        return jsonify({"error": error}), 400

    model = _load_model()

    try:
        prediction = float(model.predict(X)[0])
    except Exception:
        return jsonify({"error": "Prediction failed."}), 500

    return jsonify({"predicted_salary": round(prediction, 2)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
