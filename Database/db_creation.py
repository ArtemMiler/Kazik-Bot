import asyncio
from datetime import datetime, timedelta
from decimal import ROUND_DOWN, Decimal

from sqlalchemy import Column, Integer, Numeric, select, update
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase

from Logic.Settings import BALANCE, MIN_BET

DATABASE_URL = "sqlite+aiosqlite:///users.db"
engine = create_async_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


class UserData(Base):
    __tablename__ = "user_data"

    chat_id = Column(Integer, primary_key=True)
    balance = Column(Numeric(10, 2), default=BALANCE)
    bet = Column(Numeric(10, 2), default=MIN_BET)
    main_message_id = Column(Integer, nullable=True)
    free_spin = Column(Integer, default=-1)


async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_tables():
    async with engine.begin() as eng:
        await eng.run_sync(Base.metadata.create_all)


async def get_user_data(chat_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(UserData).where(UserData.chat_id == chat_id))
            return result.scalar_one_or_none()


async def add_user_data(chat_id: int):
    async with async_session() as session:
        async with session.begin():
            new_user = UserData(chat_id=chat_id)
            session.add(new_user)
            await session.commit()


async def add_user_chat_id(chat_id: int):
    async with async_session() as session:
        async with session.begin():
            new_user = UserData(chat_id=chat_id)
            session.add(new_user)
            await session.commit()


async def update_bet(chat_id: int, new_bet: float):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(UserData).where(UserData.chat_id == chat_id)
                .values(bet=new_bet)
            )
            await session.commit()


async def add_balance(chat_id: int, new_balance: float):
    async with async_session() as session:
        async with session.begin():
            new_balance = Decimal(str(new_balance)).quantize(Decimal("0.01"), rounding=ROUND_DOWN)

            await session.execute(
                update(UserData)
                .where(UserData.chat_id == chat_id)
                .values(balance=UserData.balance + new_balance)
            )
            await session.commit()


async def update_message_id(chat_id: int, message_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(UserData).where(UserData.chat_id == chat_id)
                .values(main_message_id=message_id)
            )
            await session.commit()


async def update_free_spin(chat_id: int, free_spin: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(UserData).where(UserData.chat_id == chat_id)
                .values(free_spin=free_spin)
            )
            await session.commit()


async def restore_balance_at_midnight():
    while True:
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = (next_midnight - now).total_seconds()

        await asyncio.sleep(seconds_until_midnight)

        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(UserData).where(UserData.balance < MIN_BET)
                )
                users = result.scalars().all()

                for user in users:
                    await session.execute(
                        update(UserData).where(UserData.chat_id == user.chat_id).values(balance=BALANCE)
                    )
