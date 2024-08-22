from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

# "postgresql+asyncpg://postgres:postgres@localhost/my_felo"
DATABASE_URL = "postgresql+asyncpg://newuser:newpassword@localhost/newdb"

# engine = create_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, pool_recycle=1800, echo=False)


Base = declarative_base()
