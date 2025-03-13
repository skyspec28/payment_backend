from sqlmodel import create_engine




POSTGRES_DATABASE_URL ='postgresql://postgres:SpectruM@localhost/fastapi'

engine = create_engine(POSTGRES_DATABASE_URL, echo=True)