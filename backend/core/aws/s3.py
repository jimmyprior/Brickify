import os
from typing import BinaryIO

import boto3 

BUCKET_NAME = os.getenv("BRICKIFY_BUCKET_NAME", "files.brickify.art") #bucket name = subdomain.brickify.art

_lambda_client = None
_s3_client = None

def get_aws_lambda_client():
    """
    returns aws client
    only loads once.

    this way it does not keep reloading for the mosaic functions that don't use it.

    -> aws client
    """
    global _lambda_client

    if _lambda_client is None:
        _lambda_client = boto3.client(
            "lambda", 
            region_name= "us-east-1"
        )

    return _lambda_client


def get_signed_s3_client():
    return boto3.client(
        "s3",
        endpoint_url= f"https://files.brickify.art",
        region_name= "us-east-1"
    )

def get_s3_client():
    """
    get brickify s3 bucket client
    """
    global _s3_client

    if _s3_client is None:
        _s3_client = boto3.client("s3")
    
    return _s3_client



def upload_file(file_obj : BinaryIO, object_name : str, content_type : str = None, bucket : str = "files.brickify.art") -> None:
    """Upload a file to an S3 bucket

    :param file_obj: File to upload
    :param object_name: S3 object name. 
    :param bucket: Bucket to upload to
    """
    args = {}
    s3_client = get_s3_client()

    if not (content_type is None):
        args["ContentType"] = content_type

    file_obj.seek(0)
    s3_client.upload_fileobj(
        file_obj, 
        bucket, 
        object_name,
        ExtraArgs=args
    )

def generate_presigned_url(object_name : str, expiration : int = 3600, download : bool = False):
    """
    object_name : str
    expiration : int = 1 hour
    """

    #s3_client = get_signed_s3_client()
    s3_client = get_s3_client()

    params = {
        "Bucket": BUCKET_NAME, 
        "Key": object_name
    }

    if download:
        params["ResponseContentDisposition"] = "attatchment"

    #https://stackoverflow.com/a/66316376/13950701 (this works! just remove the duplicate)
    #make sure endpoint_url is set with the s3 client too 

    url = s3_client.generate_presigned_url(
        "get_object",
        Params=params,
        ExpiresIn=expiration
    )

    #"ResponseContentDisposition" : "attatchment" in params to change to download
    #defaults to inline

    #remove duplicate name (idk why this works but it does)
    return url
    #return url.replace(f"/{BUCKET_NAME}", "", 1)
