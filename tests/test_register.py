import logging
import os
import time
from dotenv import load_dotenv
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlmodel import SQLModel
from app.core.utils import generate_role
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


from app.infrastructure.database.session import DataBaseSession, db
from app.infrastructure.database.repositories.user import UsersRepository
from app.infrastructure.database.orm_models.users import Users
from main import app
import sys

import logging
logging.basicConfig()

sys.path.append("..")

# Charger les variables d'environnement
load_dotenv()


# Utiliser la chaîne de connexion à la base de données de test
DB_CONFIG_TEST = os.getenv('DB_CONFIG_TEST')

# Créer une connexion de test
engine = create_async_engine(DB_CONFIG_TEST, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client  # this will return the client to the test

@pytest.fixture(scope="module")
def test_db():
    db = DataBaseSession(url=DB_CONFIG_TEST)  # Use test database config
    yield db
    db.close()

@pytest.fixture(scope="module")
def test_user():
    return {
        "username": "testuser",
        "password": "TestPassword1!",
        "email": "testuser@example.com",
        "name": "Test User",
        "birthdate": "01-01-2000",
        "gender": "MALE",
        "profile_picture": "base64",
    }

def test_register_user(test_app, test_user):
    response = test_app.post("/auth/register", json=test_user)
    assert response.status_code == 200
    assert response.json()["detail"] == "Successfully save data!"


