import asyncio
import asyncpg
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler_di import ContextSchedulerDecorator
from core.middleware import settings, dbmiddleware
from core.utils.commands import set_commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from core.handlers.scheduler import form_router


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.settings.bots.admin_id, 'היי! אני בוט מתזמן. כדי לקבוע את הפגישה  הבאה שלך תקיש /start')

async def stop_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.settings.bots.admin_id, 'ביי')
    


async def create_pool():
    return await asyncpg.create_pool(
        user='postgres',
        password='marsik19',
        host='127.0.0.1',
        port='5432',
        database='schedule',
        command_timeout=60
    )


async def start():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=settings.settings.bots.token, parse_mode=ParseMode.HTML)

    try:    
        storage = RedisStorage.from_url('redis://localhost:6379/0')
        print('Redis connected!')
    except Exception as e:
        logging.exception(f"Exception during connection to redis: {e}")

    try:
        jobstores = {
            'default': RedisJobStore(jobs_key='dispatched_trips_jobs',
                                    run_times_key='dispatched_trips_running',
                                    host='localhost',
                                    port=6379,
                                    db=2
                                    )
        }
        print('Jobstores created!')
    except Exception as e:
        logging.exception(f"Exception during creating jobstores: {e}")

    try:
        scheduler = ContextSchedulerDecorator(AsyncIOScheduler(timezone='Europe/Kiev', jobstores=jobstores))
        scheduler.ctx.add_instance(bot, declared_class=Bot)
        scheduler.start()
        print('Scheduler started!')
    except Exception as e:
        logging.exception(f"Exception during creating scheduler: {e}")
   
    try:
        dp = Dispatcher(storage=storage)
        print('Dispatcher created!')
    except Exception as e:
        logging.exception(f"Exception during creating dispatcher: {e}")

    try:
        pool = await create_pool()
        dp.update.middleware.register(dbmiddleware.DbSession(pool))
        dp.startup.register(start_bot)
        dp.shutdown.register(stop_bot)

        dp.include_router(form_router)
    except Exception as err:
        logging.error(err)

    try:
        await dp.start_polling(bot)
        print('Polling started!')
    except Exception as err:
        logging.error(err)
    finally:
        await stop_bot(bot)


if __name__ == '__main__':
    logging.basicConfig(filename='bot.log', level=logging.INFO)
    asyncio.run(start())