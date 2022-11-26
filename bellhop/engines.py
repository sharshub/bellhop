import os
import boto3
from botocore.client import Config
import mimetypes


class Engine:
    def object_url(self, model_name, model_id):
        raise NotImplementedError("Object object_url method not implemented")

    def save(self, model_name, model_id, file):
        raise NotImplementedError("Object save method not implemented")

    def delete(self, model_name, model_id):
        raise NotImplementedError("Object delete method not implemented")


class AWSEngine(Engine):
    def __init__(self, **kwargs):
        AWS_ACCESS_KEY_ID = kwargs.pop("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = kwargs.pop("AWS_SECRET_ACCESS_KEY")
        self.bucket_name = kwargs.pop("S3_BUCKET")
        self.s3_region = kwargs.pop("S3_REGION")
        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3_client = boto3.client(
            "s3",
            region_name=self.s3_region,
            config=Config(signature_version="s3v4"),
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = self.s3.Bucket(self.bucket_name)

    def object_url(self, model_name, object_id, object_name):
        return self.s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": "%s_uploads/%s/%s" % (model_name, object_id, object_name),
            },
            ExpiresIn=3600,
        )

    def save(self, model_name, object_id, file):
        self.delete(model_name, object_id)
        mime_type = mimetypes.guess_type(file.name)[0]
        file_path = "%s_uploads/%s/%s" % (
            model_name,
            object_id,
            os.path.basename(file.name),
        )
        self.bucket.upload_file(
            file.name,
            file_path,
            ExtraArgs={
                "ContentType": mime_type if mime_type else "binary/octet-stream"
            },
        )

    def delete(self, model_name, object_id):
        folder_path = "%s_uploads/%s/" % (model_name, object_id)
        self.bucket.objects.filter(Prefix=folder_path).delete()
