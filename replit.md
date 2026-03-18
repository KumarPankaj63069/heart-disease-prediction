# Heart Disease Prediction App

A Flask web application that uses machine learning to predict heart disease risk based on patient data.

## Architecture

- **Backend**: Python / Flask
- **ML Model**: scikit-learn RandomForestClassifier (pre-trained, stored in `model.pkl`)
- **Database**: SQLite (`database.db`) — stores users and prediction history
- **Templates**: Jinja2 HTML templates in `/templates`
- **Static Assets**: `/static/images`

## Key Files

- `app.py` — Main Flask application with all routes
- `model.pkl` — Pre-trained ML model
- `features.pkl` — Feature names used by the model
- `train_model.py` — Script to retrain the model from `heart.csv`
- `database.db` — SQLite database (users + history)

## Features

- User registration and login (session-based auth)
- Heart disease risk prediction form
- Prediction history per user
- About page

## Running Locally

```bash
python app.py
```

Runs on `0.0.0.0:5000`.

## Deployment

Uses Gunicorn for production:
```bash
gunicorn --bind=0.0.0.0:5000 --reuse-port app:app
```

## Dependencies

Managed via `uv` / `pyproject.toml`:
- flask
- numpy
- scikit-learn
- gunicorn
