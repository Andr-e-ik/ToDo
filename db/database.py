from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = ""

engine = create_async_engine(DATABASE_URL, pool_recycle=1800, echo=False)


Base = declarative_base()
