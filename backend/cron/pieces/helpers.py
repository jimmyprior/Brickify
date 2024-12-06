import re 
import logging
from typing import Iterator

from brickpy import Color

from .api import Rebrickable


def parse_color_data_from_rebrick(raw_color_data : list[dict]) -> Iterator[dict]:
	"""
	generator (yields colors)
	resp: {
			"name" : rebrickable_name,
			"transparent" : color_data["is_trans"],
			"spaces" : {
				"rgb" :	color_obj.rgb,
				"cielab" : color_obj.lab
			},
			"ids" : external_data["ids"],
			"names" : external_data["names"]
	}

	gets colors from rebrickable, yeilds each parsed color
	"""

	def parse_external_data(color_data : dict) -> dict:
		"""
		external name: BrickLink, LEGO, BrickOwl
		
		return -> {
			ids : {lego : "", bricklink : "", ...},
			names : {lego : "", bricklink : "", ...}
		}
		"""
		output = {
			"ids" : {},
			"names" : {}
		}

		EXTERNAL_SITES = ["BrickLink", "BrickOwl", "LEGO"]

		external_data = color_data["external_ids"]
		
		for site_name in EXTERNAL_SITES:
			data = external_data.get(site_name, {})
			ext_name = data.get("ext_descrs", [[None]])[0][0]
			ext_id = data.get("ext_ids", [None])[0]

			output["names"][site_name.lower()] = ext_name
			output["ids"][site_name.lower()] = ext_id

		return output


	for raw_color in raw_color_data:
		#loop through the raw color data and parse it for brickify
		rebrickable_id = raw_color["id"]
		rebrickable_name = raw_color["name"]

		#rebrickable has data for wierd "fake" pieces with ids outside of this range. Just skip them
		if rebrickable_id < 0 or rebrickable_id == 9999:
			logging.info(f"Skipped color {rebrickable_name}:{rebrickable_id}. ID out of range.")
			continue

		#use brickpy color to get rgb and hex
		color_obj = Color.from_hex(raw_color["rgb"], rebrickable_name)

		#the external name and id fields are nested into lists so get them out of the lists:
		external_data = parse_external_data(raw_color)
		external_data["ids"]["rebrickable"] = rebrickable_id
		external_data["names"]["rebrickable"] = rebrickable_name

		#only add colors that contain bricklink and brickowl ids (requried for some functionality)
		#FIX THIS TO ADD BRICKOWL 
		ex_ids = external_data["ids"]
		if (ex_ids["bricklink"] is None) or (ex_ids["brickowl"] is None):
			#must have bricklink id and brickowl to get added
			logging.info(f"Skipped color {rebrickable_name}:{rebrickable_id}. Missing external IDs.")
			continue
		
		yield {
			"name" : rebrickable_name,
			"transparent" : raw_color["is_trans"],
			"spaces" : {
				"rgb" :	color_obj.rgb,
				"cielab" : color_obj.lab
			},
			"ids" : external_data["ids"],
			"names" : external_data["names"],
		}


async def get_color_data(api : Rebrickable) -> Iterator[dict]:
	"""
	request color data from rebricakble, parse and yield it.
	"""
	try:
		#500 is enough to fit all the colors at the moment. Defaults to 30 if not specified
		resp = await api.get_colors(page_size=500)
		raw_color_data = resp["results"]
	except KeyError:
		logging.exception("Failed to get color data")
		raise

	for color in parse_color_data_from_rebrick(raw_color_data):
		yield color
	

def parse_plate_data_from_rebrick(raw_plate_data : list[dict]) -> Iterator[dict]:
	"""
	
	"""
	def get_plate_size(part_name : str) -> tuple | None:
		"""
		returns the size of a plate by using a regex expression on the part name
		returns None if plate name is invalid or tuple of plate size otherwise

		valid:
			Plate 4 x 4
			Plate 10 x 6
		invalid:
			Plate 4 x 4 with holes
		"""
		pattern = r"Plate (\d+) x (\d+)$"
		match = re.match(pattern, part_name)
		if match is None:
			return match
		return (int(match.group(1)), int(match.group(2)))


	def parse_part_id(ids : list[str]) -> str | None:
		"""
		sometimes the id is a nested list, sometime not. 
		Parse it accordingly
		"""
		if len(ids) > 0:
			return str(ids[0])
		return None


	for raw_plate in raw_plate_data:

		rebrickable_name = raw_plate["name"]

		rebrickable_id = str(raw_plate["part_num"])	
		lego_id = parse_part_id(raw_plate["external_ids"].get("LEGO", []))
		bricklink_id = parse_part_id(raw_plate["external_ids"].get("BrickLink", []))
		brickowl_id = parse_part_id(raw_plate["external_ids"].get("BrickOwl", []))

		if (bricklink_id is None) or (rebrickable_id is None) or (brickowl_id is None):
			#must have these to be considered a valid piece
			logging.info(f"Skipped plate {rebrickable_name}:{rebrickable_id}. Missing external IDs.")
			continue

		size = get_plate_size(rebrickable_name)

		#if size is invalid skip piece. See parser for info on what is classified as invalid
		if size is None:
			logging.info(f"Skipped plate {rebrickable_name}:{rebrickable_id}. Invalid name/size.")
			continue

		yield {
			"name": rebrickable_name,
			"group": "PLATE",
			"ids": {
				"lego": lego_id,
				"rebrickable": rebrickable_id,
				"bricklink": bricklink_id,
				"brickowl": brickowl_id
			},
			"size": [size[0], size[1]]
		}


async def get_plate_data(api : Rebrickable) -> Iterator[dict]:
	"""
	
	"""
	REBRICKABLE_PLATE_CAT_ID = 14
	try:
		#500 is enough to fit all the plates at the moment. Defaults to 30 if not specified
		resp = await api.get_parts(
			page_size=500, 
			part_cat_id=REBRICKABLE_PLATE_CAT_ID
		)
		raw_plate_data = resp["results"]
	except KeyError:
		logging.exception("Failed to get plate data")
		raise

	for plate in parse_plate_data_from_rebrick(raw_plate_data):
		yield plate


async def get_piece_data(api : Rebrickable, colors : dict, plates : dict) -> Iterator[dict]:
	"""
	colors: {uuid : {...}, uuid : {...}
	plates: {uuid : {...}, uuid : {...}
	"""
	#creates new dict that corresponds rebrickids to uuids
	rebrick_index = lambda data : dict((d["ids"]["rebrickable"], _uuid) for _uuid, d in data.items())

	#{rebrick_id : uuid, rebrick_id : uuid}
	colors_rebrick_indexable = rebrick_index(colors)
	plates_rebrick_indexable = rebrick_index(plates)

	for rebrickable_plate_id, brickify_plate_uuid in plates_rebrick_indexable.items():
		#loop through each plate, find all the colors it comes in
		resp = await api.get_part_colors(rebrickable_plate_id, page_size = 500)
		colors_brief = resp["results"]
		#relate those colors to the full data from rebrickable id
		for raw_brief_data in colors_brief:
			#get the rebrickable color_data
			rebrickable_color_id = raw_brief_data["color_id"]

			#get info about the color plate combo (set usage, production years)
			resp = await api.get_part_color_combo(rebrickable_plate_id, rebrickable_color_id)

			#parse usage and production data
			year_start = resp.get("year_from")
			year_end = resp.get("year_to")
			num_sets = resp.get("num_sets")
			num_in_sets = resp.get("num_set_parts")

			#skip if it doesn't have usage or production data
			if None in [year_start, year_end, num_sets, num_in_sets]:
				logging.info(f"Skipped piece with plate #{rebrickable_plate_id} and color #{rebrickable_color_id}. Invalid usage or production data.")
				continue

			brickify_color_uuid = colors_rebrick_indexable.get(rebrickable_color_id)
			if brickify_color_uuid is None:
				#must have a valid color to be added
				logging.info(f"Skipped piece with plate #{rebrickable_plate_id} and color #{rebrickable_color_id}. Could not find color data")
				continue 
			
			#because uuid is key have to access it this wierd way
			yield {
				"color_uuid" : brickify_color_uuid,
				"part_uuid" : brickify_plate_uuid,
				"usage" : {
					"num_sets" : int(num_sets),
					"num_in_sets" : int(num_in_sets)
				},
				"production" : {
					"start" : int(year_start),
					"end" : int(year_end)
				}
			}
