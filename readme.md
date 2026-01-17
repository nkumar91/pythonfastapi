# CRAETE A VIRTUAL ENVIORNMENT
python -m venv venv

# ACTIVATE A VIRTUAL ENV
.\venv\Scripts\activate

# DEACTIVATE  A VIRTUAL ENV
.\venv\Scripts\activate

# CRAETE DEPENDENCY
pip freeze > requirements.txt

# BUILD DOCKER IMAGE / CRAETE DOCKER IMAGE
docker build -t pythonfastapi  .   

# CRAETE BUILD CONTAINER 
docker run -d --name pyfirstcon(Container_name) -p 8000:8000 pythonfastapi (build name) 

# RUN SERVER
uvicorn app.main:app --reload

# CRAETE FAST API PROJECT FIRST TIME
pip install fastapi uvicorn python-dotenv

# FOLDER STRUCTURE
fastapi_project/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes.py
│   │
│   ├── models/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   └── __init__.py
│   │
│   ├── services/
│   │   └── __init__.py
│   │
│   └── db/
│       ├── __init__.py
│       └── session.py
│
├── .env
├── requirements.txt
└── run.py

