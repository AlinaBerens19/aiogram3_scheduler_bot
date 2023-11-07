import asyncpg
from asyncpg import Record
from typing import List




class Request:
    def __init__(self, connector):
        self.connector = connector

    async def get_meetings(self, user_id: int) -> List[Record]:
        sql = "SELECT * FROM schedule WHERE user_id = $1"
        return await self.connector.fetch(sql, user_id) 

    async def delete_meeting(self, id: int) -> None:
        sql = "DELETE FROM schedule WHERE id = $1"
        await self.connector.execute(sql, id)   

    async def create_meeting(self, name: str, week: str, day: str, time: str, user_id: int) -> None:
        sql = "INSERT INTO schedule (name, week, day, time, user_id) VALUES ($1, $2, $3, $4, $5)"
        await self.connector.execute(sql, name, week, day, time, user_id)
