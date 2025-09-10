# ShvikiFitness Membership App

## Quick start (without Docker)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py

## Using Docker Compose
cp .env.example .env
docker compose up --build

- Register via `/register`
- Login via `/login`
- Dashboard at `/dashboard`
