from database.database import engine
from database import models

# Create all tables based on models
models.Base.metadata.create_all(bind=engine)
