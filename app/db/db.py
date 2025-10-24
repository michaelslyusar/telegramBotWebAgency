from sqlalchemy import BigInteger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///users.db", echo=False, future=True)
async_session = async_sessionmaker(engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]

class Request(Base):
    __tablename__ = "requests"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    service: Mapped[str]
    description: Mapped[str]

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    product: Mapped[str]
    company_description: Mapped[str]
    services_required: Mapped[str]


# Async engine for SQLite
async def async_main():
    async with engine.begin() as conn :
        await conn.run_sync(Base.metadata.create_all)

