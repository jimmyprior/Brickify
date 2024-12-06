import json
import logging
from urllib.parse import urlencode

import aiohttp
import oauthlib.oauth1

from .types import (
    ItemType, GuideType, 
    Condition, Country, 
    Currency, Region
)

logging.getLogger('aiohttp').setLevel(logging.WARNING)
logging.getLogger('oauthlib').setLevel(logging.WARNING)

BASE_URL = "https://api.bricklink.com/api/store/v1"


def strip_null_from_dictionary(dictionary : dict):
    """
    strip null values from a dictionary

    I think I can get rid of this.
    """
    for key in list(dictionary.keys()):
        if dictionary[key] is None:
            dictionary.pop(key)

    return dictionary



class BrickLink:

    def __init__(
        self, 
        consumer_key : str, 
        consumer_secret : str, 
        token_value : str, 
        token_secret : str
        ):
        
        self.oauth = oauthlib.oauth1.Client(
            client_key = consumer_key,
            client_secret = consumer_secret,
            resource_owner_key = token_value,
            resource_owner_secret = token_secret
        )

    async def request(self, method : str, endpoint : str, query : dict = {}):
        """
        method : 
        endpoint : 
        query : 
        """

        strip_null_from_dictionary(query)

        url_encoded_params = urlencode(query)

        uri, headers = self.oauth.sign(
            uri = BASE_URL + endpoint + "?" + url_encoded_params,
            http_method = method
        )[:2]

        logging.debug(f"Making request. Endpoint: {endpoint} Query: {json.dumps(query)}")


        async with aiohttp.ClientSession() as session:
            async with session.request(method, uri, headers=headers) as r:

                status = r.status
                resp = await r.json(content_type=None)

                logging.debug(f"Request Response. Endpoint: {endpoint}, Query: {json.dumps(query)}, Resp: {json.dumps(resp)}, Status : {status}")
                #if status 
                
                return resp["data"]


    async def get_item_price_data(
        self, 
        item_type : ItemType, 
        item_id : str,
        color_id : int = None,
        guide_type : GuideType = None,
        condition : Condition = None,
        country_code : Country = None,
        region : Region = None,
        currency_code : Currency = None,
        ):

            
        """
        type	String	N	The type of the item. Acceptable values are:
        MINIFIG, PART, SET, BOOK, GEAR, CATALOG, INSTRUCTION, UNSORTED_LOT, ORIGINAL_BOX
        no	String	N	Identification number of the item
        color_id	Integer	Y	The color of the item
        guide_type	String	Y	Indicates that which statistics to be provided. Acceptable values are:
        - "sold": Gets the price statistics of "Last 6 Months Sales"
        - "stock": Gets the price statistics of "Current Items for Sale" (default)
        new_or_used	String	Y	Indicates the condition of items that are included in the statistics. Acceptable values are:
        - "N": new item (default)
        - "U": used item
        country_code	String	Y	The result includes only items in stores which are located in specified country.
        - If you don't specify both country_code and region, this method retrieves the price information regardless of the store's location
        region	String	Y	The result includes only items in stores which are located in specified region.
        - Available values are: asia, africa, north_america, south_america, middle_east, europe, eu, oceania
        - If you don't specify both country_code and region, this method retrieves the price information regardless of the store's location
        currency_code	String	Y	This method returns price in the specified currency code
        - If you don't specify this value, price is retrieved in the base currency of the user profile's
        vat	String	Y	Indicates that price will include VAT for the items of VAT enabled stores. Available values are:
        - "N": Exclude VAT (default)
        - "Y": Include VAT
        - "O": Include VAT as Norway settings

        -> {
            "item": {
                "no":"7644-1",
                "type":"PART" 
            },
            "new_or_used":"N",
            "currency_code":"USD",
            "min_price":"96.0440",
            "max_price":"695.9884",
            "avg_price":"162.3401",
            "qty_avg_price":"155.3686",
            "unit_quantity":298,
            "total_quantity":359,
            "price_detail": [
            ]
        }
        """

        query = {
            "color_id" : color_id,
            "guide_type" : guide_type,
            "new_or_used" : condition,
            "country_code" : country_code,
            "region" : region,
            "currency_code" : currency_code
        }

        return await self.request("GET", f"/items/{item_type}/{item_id}/price", query)




