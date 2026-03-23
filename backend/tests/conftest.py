import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api.deps import get_db

# 1. Configuration d'une base de données SQLite jetable pour les tests
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_phytoscan.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# On crée les tables
Base.metadata.create_all(bind=engine)

# 2. On remplace la dépendance "get_db" de FastAPI par la nôtre
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 3. Client de test FastAPI (Comme Postman, mais en Python)
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c