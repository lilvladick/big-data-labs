from sqlalchemy import create_engine
from models import Base

engine = create_engine("postgresql://admin:admin@database:5432/sakila",echo=True)
Base.metadata.create_all(engine)
