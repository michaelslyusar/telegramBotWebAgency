from app.db.db import async_session
from app.db.db import User,Request
from sqlalchemy import select
from loguru import logger

async def set_user(tg_id,first_name,last_name,email) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            try:
                session.add(User(tg_id=tg_id, first_name=first_name, last_name=last_name, email=email))
                await session.commit()
                logger.info(f'User [{tg_id} : {first_name} {last_name} - Email:{email}] was registered successfully')
            except Exception as e:
                logger.error(f'Error occured while inserting user to DB : {e}')

async def set_new_request(tg_id,first_name,last_name,email,service,description) -> None:
    async with async_session() as session:
        try:
            session.add(Request(tg_id=tg_id, first_name=first_name, last_name=last_name, email=email,description=description,service=service))
            await session.commit()
            logger.info(f'Request [{tg_id} : Email - {email} Service - {service}] was registered successfully')
        except Exception as e:
            logger.error(f'Error occured while inserting request to DB : {e}')


