import json 
import uuid
import time 
import types
import typing
import logging
import dataclasses 

from motor.core import AgnosticDatabase, AgnosticCollection
from pydantic import ValidationError

class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)

            return super().default(o)


def get_true_type(type_):
    """
    strips away optional and iterable types to access the real type.
    this is used to access any required mongodb aggregate stuff.
    """
    args = typing.get_args(type_)
    origin = typing.get_origin(type_)
    
    if origin is None:
        #is base type
        return type_
    elif origin in (typing.Union, types.UnionType):
        #if two valid types returns the first
        #strip none types and return first (send again to make sure not iterable)
        return get_true_type([i for i in args if i != types.NoneType][0])
    elif "__iter__" in vars(type_):
        #return first in iterable
        return args[0]


def get_projection(obj) -> dict:
    """
    model : uninitialized dataclass
    gets the projection for a model
    returns projection in mongodb aggregate stage format

    -> {
        '$project': {
            'piecelist.part.test': True, 
            'piecelist.test': True, 
            'hello': True, 
            'other': True
        }
    }
    """
    projection = {"_id" : False}
    def recursive_add_model(obj, projection : dict):
        """
        obj : dataclass 
        projection : dictionary of the projection
        """
        #gets type names and types
        annotations = vars(obj).get("__annotations__", False)
        if annotations:
            for field_name, field_type in annotations.items():
                #parses types that obsure true type (optional, or, iterative type (list, set, tuple))
                true_type = get_true_type(field_type)
                if dataclasses.is_dataclass(true_type): #if the true type is a dataclass, means there are sub fields and should resursivly add 
                    projection_ref = {}
                    recursive_add_model(true_type, projection_ref) #modifies pipeline and projection ref
                    for key, item in projection_ref.items(): #adds the projection
                        projection[f"{field_name}.{key}"] = item
                else:
                    projection[field_name] = True            

    recursive_add_model(obj, projection)
    return {"$project" : projection}


Model = typing.TypeVar("Model")

async def get_documents(
    model : typing.Type[Model], 
    database : AgnosticDatabase,
    pipeline : list = []
    ) -> list[Model]:
    """
    model: datacalss that should be returned 
            see list of dataclass models in the file
            each model has special aggregate queries 
            to only query necessary fields to prevent 
            unnecessary bandwidth usage. must have "AGGREGATE" 
            and "COLLECTION" class vars set to work correctly.
    db  : async database connection
    **kwargs (match query) creates the match query
    """
    pipeline.extend(model.AGGREGATE)
    pipeline.append(get_projection(model))
    collection = database[model.COLLECTION]
    models = []
    logging.info(f"Executing db query for model {str(model)}")
    async for doc in collection.aggregate(pipeline):
        try:
            models.append(model(**doc))
        except ValidationError as e:
            #need to make this work for uuids
            logging.debug(f"Pipeline: {json.dumps(doc, cls=EnhancedJSONEncoder)}")
            logging.debug(f"Model: {str(model)}")
            logging.debug(f"DB Response: {json.dumps(doc, cls=EnhancedJSONEncoder)}")
            logging.debug("Database response did not match Dataclass")
            raise e
        
    return models 


class ModelDoesNotExist(Exception):
    """
    model does not exist
    """
    pass


async def get_document(
    model : typing.Type[Model], 
    database : AgnosticDatabase,
    pipeline : list = []
    ) -> Model:
    """
    throws no model exist if no documents are returned
    """
    models = await get_documents(model, database, pipeline)
    if len(models) > 0:
        return models[0]
    raise ModelDoesNotExist


def dataclass_to_dict(obj):
    """
    need to convert the dataclasses back to dicts
    """
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    elif "__iter__" in vars(type(obj)) and (type(obj) in [list, set, tuple]):
        #this needs to be fixed big time!!
        return [dataclass_to_dict(o) for o in obj]
    else:
        return obj
    

async def upload_document(
    document : dict, 
    collection : AgnosticCollection
    ) -> uuid.UUID:
    """
    upload a document to a collection
    """
    #need to turn data classes to dicts so..
    for key, value in document.items():
        document[key] = dataclass_to_dict(value)
    
    _uuid = uuid.uuid4()
    document["uuid"] = _uuid
    document["created"] = int(time.time())
    _id = await collection.insert_one(document)
    return _uuid