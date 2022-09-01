import asyncio

import uvloop
from sqlalchemy import select

from . import models
from .db import SessionLocal

class CrudMethods:
    def __init__(self):
        self.self = self
        
    async def get_all_commands(self):
        """Gets all of the commands from the DB
        """
        async with SessionLocal() as session:
            async with session.begin():
                selectItem = select(models.HelpData)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    
    async def get_all_commands_from_module(self, module: str):
        """Gets all of the commands from a specific module

        Args:
            module (str): The module to get the commands from

        Returns:
            list: List of commands
        """
        async with SessionLocal() as session:
            async with session.begin():
                selectItem = select(models.HelpData).filter(models.HelpData.module == module)
                res = await session.execute(selectItem)
                return [row for row in res.scalars()]
            
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())