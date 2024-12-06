import os 
import time
import asyncio
import json
import logging 
from uuid import UUID 

from dataclasses import dataclass

from .bricklink.api import BrickLink
from .bricklink.types import ItemType, GuideType, Condition

#need to update this to use the new core
from ...core.database.database import Database
from ...core.database.builder import get_document, get_documents
from ...core.objects.piece.database import piece_query, PiecePriceData, PriceData


#database models
@dataclass
class BLIDModel:
    bricklink : str

@dataclass
class BLPartModel:
    size : tuple[int, int]
    ids : BLIDModel

@dataclass
class BLColorModel:
    ids : BLIDModel

@dataclass
class SimplePriceModel:
    scraped : int

@dataclass
class BrickLinkPiece:
    uuid : UUID
    part : BLPartModel
    color : BLColorModel
    price : SimplePriceModel = None


def chunk_iterable(l : list, n : int):
    """
    chunk an iterable l into n size chunks
    """
    for i in range(0, len(l), n): 
        yield l[i:i + n]


class Bot:
    def __init__(self):
        
        self.bricklink = BrickLink(
            os.getenv("CLIENT_KEY"),
            os.getenv("CLIENT_SECRET"),
            os.getenv("RESOURCE_OWNER_KEY"),
            os.getenv("RESOURCE_OWNER_SECRET")
        )
        self.max_age = 7 * 24 * 60 * 60 #rescrape after one week
        self.batch_size = 4 #how many pieces to scrape per async batch. 
        #Two requests are made for each piece (two condition)
        #make sure to abide by bricklink rate limits per day. 5000 I think.
        self.batch_wait = 5 #wait 5 seconds between each batch


    async def get_price_data(
        self,
        bricklink_part_id : str, 
        bricklink_color_id : str,
        condition : Condition,
        guide_type : GuideType = GuideType.STOCK
        ) -> dict | None:
        """
        gets price data from bricklink. Returns dictionary with data
        -> {
            min : float
            max : float
            avg : float
        }
        or 
        None
        """
        
        try: 
            #get the price data from the api
            price_data = await self.bricklink.get_item_price_data(
                ItemType.PART,
                item_id = bricklink_part_id,
                color_id = bricklink_color_id,
                guide_type = guide_type,
                condition = condition
            )
            logging.debug(f"Raw price data for {condition} {bricklink_part_id}: {json.dumps(price_data)}")


        except Exception as e:
            #maybe get rid of this try except 
            #log exception and reason
            logging.exception(f"Exception for piece {condition} {bricklink_part_id} {bricklink_color_id}")
            return None
        
        
        output = {
            "min" : float(price_data.get("min_price", 0)),
            "max" : float(price_data.get("max_price", 0)),
            "avg" : float(price_data.get("avg_price", 0))
        }

        #if piece is missing any price field return None
        for key, value in output.items():
            if value == 0:
                logging.warning(f"Missing {key} price for piece {condition} {bricklink_part_id}")
                return None

        return output

    
    async def add_piece_to_database(self, db : Database,  piece : BrickLinkPiece) -> bool:
        """
        makes two requests to get new and used price data and adds 
        it to the database 
        """
        price_data = {"scraped" : int(time.time())}
        #get price data for both use condition and new condition
        for name, condition in [("new", Condition.NEW), ("used", Condition.USED)]:
            
            #get price data from bricklink
            #gets it for currently in stock pieces but could swap out for histroical
            condition_data = await self.get_price_data(
                bricklink_part_id = piece.part.ids.bricklink, 
                bricklink_color_id = piece.color.ids.bricklink,
                condition = condition,
                guide_type = GuideType.STOCK
            )

            if condition_data is None:
                #failed to get price data for this thing and not adding it
                return False
            
            #add price per stud to the data using part area
            area = piece.part.size[0] * piece.part.size[1]
            condition_data["pps"] = round(condition_data["avg"] / area, 4)
            
            price_data[name] = condition_data
            
        logging.debug(f"Price data to be inserted into db for {piece.uuid}: {json.dumps(price_data)}")

        #insert into the database 
        await db.piece_collection.update_one(
            {"uuid" : piece.uuid},
            {"$push": {"pricing": price_data} }
        )

        logging.info(f"Added price data for piece {piece.uuid} to the database")
        return True


    async def run(self):
        db = Database()

        #get all the pieces from the database 
        pieces = await get_documents(
            model = BrickLinkPiece,
            collection = db.piece_collection,
            query = piece_query
        )   
        logging.info(f"Retrieved {len(pieces)} pieces from database")

        async def scrape_coroutine(piece):
            current_time = int(time.time())
            #don't scrape if the data isn't older than max age 
            #price is always the most updated data
            #scrape price data if there is no current data or time since last scrape is greater than max age
            if (piece.price is None) or (current_time - piece.price.scraped) > self.max_age:
                await self.add_piece_to_database(db=db, piece=piece)
            else:
                logging.info(f"Skipping piece {piece.uuid}. Data is within max age")
                return None

        #chunk into batches of some size to take aadvantage of async
        batched_pieces = list(chunk_iterable(pieces, self.batch_size))
        for index, pieces_batch in enumerate(batched_pieces):
            await asyncio.gather(*[scrape_coroutine(piece) for piece in pieces_batch])
            logging.info(f"Completed batch {index}/{len(batched_pieces)}")
            await asyncio.sleep(self.batch_wait) #wait after each batch

        #non async
        # for piece in pieces[:10]:
        #     await scrape_coroutine(piece)



async def main(filename : str = None):

    logging.basicConfig(
        filename=f'{filename}.log', 
        encoding='utf-8', 
        level=logging.INFO, 
        format='[%(asctime)s] %(levelname)s:%(message)s'
    )

    bot = Bot() 
    await bot.run()


asyncio.run(main())