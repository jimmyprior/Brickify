import logging
import asyncio
import json 
import re 

from aiohttp import ClientSession

def remove_bad_parms(params : dict, remove : set = {"self"}):
	modified_params = {}
	for key, val in params.items():
		if not (key in remove) and not (val is None):
			modified_params[key] = val
	return modified_params


class Rebrickable:
	def __init__(self, api_key : str):
		self.requst_wait_period = 1 #seconds (avoid rate limit)
		self.api_key = api_key  
		self.session = ClientSession(
			base_url="https://rebrickable.com"
		)

	async def request(self, method : str, endpoint : str, **kwargs):
		logging.debug(f"REQUEST: {method} {endpoint}")
		await asyncio.sleep(self.requst_wait_period)
		resp = await self.session.request(
			method, 
			endpoint, 
			headers={
				"Authorization": f"key {self.api_key}"
			},
			**kwargs
			)
		data = await resp.json()
		status_code = int(resp.status)
		if status_code >= 400:
			logging.warning(f"UNSUCCESSFUL RESPONSE: {status_code}. Data: {json.dumps(data, indent=2)}")

			if status_code == 429:
				#body example: {detail: Request was throttled. Expected available in 6 seconds.}
				match = re.findall(r'\b\d+\b', data["detail"])
				delay = int(match.group(1))
				logging.info(f"Request Throttled. Sleeping for {delay} seconds")
				await asyncio.sleep(delay)	
				self.request(method, endpoint, **kwargs) #retry the request
			
		return data
        
		
	async def get_categories(
        self, 
        page : int = None, 
        page_size : int = None, 
        ordering : str = None
        ):
		"""
		Get a list of all Part Categories.
		"""
		params = remove_bad_parms(locals())
		endpoint = "/api/v3/lego/part_categories"
		return await self.request("GET", endpoint, params=params)


	async def get_colors(
        self, 
        page : int = None, 
        page_size : int = None, 
        ordering : str = None
		):
		params = remove_bad_parms(locals())
		endpoint = "/api/v3/lego/colors"
		return await self.request("GET", endpoint, params=params)


	async def get_parts(
		self,
		page : int = None,
		page_size : int = None,
		part_num : str = None,
		part_nums : str = None,
		part_cat_id : str = None,
		color_id : str = None,
		bricklink_id : str = None,
		brickowl_id : str = None,
		lego_id : str = None,
		ldraw_id : str = None,
		ordering : str = None,
		search : str = None
		):
		params = remove_bad_parms(locals())
		endpoint = "/api/v3/lego/parts"
		return await self.request("GET", endpoint, params=params)


	async def get_part(
		self,
		part_num : str
		):
		endpoint = f"/api/v3/lego/parts/{part_num}"
		return await self.request("GET", endpoint)


	async def get_part_colors(
		self, 
		part_num : str, 
		page : int = None,
		page_size : int = None,
		ordering : str = None
		):
		"""
		-> {
			"count": 14,
			"next": null,
			"previous": null,
			"results": [
				{
					"color_id": 0,
					"color_name": "Black",
					"num_sets": 134,
					"num_set_parts": 463,
					"part_img_url": "https://cdn.rebrickable.com/media/parts/elements/6174917.jpg",
					"elements": [
						"6174917"
					]
				},
			]
		}
		"""
		params = remove_bad_parms(locals(), {"self", "part_num"})
		endpoint = f"/api/v3/lego/parts/{part_num}/colors"
		return await self.request("GET", endpoint, params=params)

	async def get_part_color_combo(
		self, 
		part_id : str,
		color_id : str
		):
		"""
		resp -> 
		{
			"part_img_url": "https://cdn.rebrickable.com/media/parts/elements/6174917.jpg",
			"year_from": 2016,
			"year_to": 2023,
			"num_sets": 134,
			"num_set_parts": 463,
			"elements": [
				"6174917"
			]
		}
		"""
		endpoint = f"/api/v3/lego/parts/{part_id}/colors/{color_id}"
		return await self.request("GET", endpoint)


	async def close(self):
		await self.session.close()


