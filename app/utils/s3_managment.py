# app/utils/s3_manager.py  ← קובץ חדש / גרסה מינימלית

import boto3
import botocore.exceptions 
from flask import current_app
from io import BytesIO


class S3Manager:

    _client = None
    _bucket = None

    @staticmethod
    def _init():
        if S3Manager._client is None:
            cfg            = current_app.config
            S3Manager._bucket  = cfg["S3_BUCKET"]
            params = {"region_name": cfg["AWS_REGION"]}
            if cfg.get("AWS_ACCESS_KEY_ID") and cfg.get("AWS_SECRET_ACCESS_KEY"):
                params.update(
                    aws_access_key_id     = cfg["AWS_ACCESS_KEY_ID"],
                    aws_secret_access_key = cfg["AWS_SECRET_ACCESS_KEY"]
                )
            S3Manager._client = boto3.client("s3", **params)

    @staticmethod
    def upload(fileobj, dest_key: str):
        S3Manager._init()
        mime = getattr(fileobj, "mimetype", "application/octet-stream")

        # --- קרא את התוכן לזיכרון כדי שלא יסגר בין ניסיונות ---
        data = fileobj.read()                                     # 🆕 ADDED
        body = BytesIO(data)                                      # 🆕 ADDED

        try:
            S3Manager._client.upload_fileobj(
                Fileobj = body,                                   # 🆕 CHANGED
                Bucket  = S3Manager._bucket,
                Key     = dest_key,
                ExtraArgs = {
                    "ContentType": mime,
                    "ServerSideEncryption": "AES256"              # 🆕 ADDED
                },
            )
        except botocore.exceptions.ClientError as e:
            # נזרוק הודעה ברורה־יותר ללוג
            import logging
            logging.error("S3 upload failed: %s", e.response)
            raise
