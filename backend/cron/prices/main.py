import asyncio
import logging

from bot import Bot


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s", 
    level=logging.DEBUG, 
    datefmt="%m/%d/%Y %I:%M:%S %p",
    handlers=[
        logging.FileHandler("pricebot.log"),
        logging.StreamHandler()
    ]
)

    await piece_collection.update_one(
        {"_id": piece_id},
        { "$push": { "pricing" : price_data} }
    )

bricklink_bot = Bot()

asyncio.run(bricklink_bot.run()) 

