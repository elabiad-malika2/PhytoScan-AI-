from sqlalchemy.orm import declarative_base

# Création de la base déclarative (que toutes les tables utilisent)
Base = declarative_base()


from app.models.user import User
from app.models.plant_scan import PlantScan
from app.models.query import Query
from app.models.report import Report