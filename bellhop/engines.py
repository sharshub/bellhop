import os
import boto3


class Engine:
    def save(self, model_name, model_id, file):
        raise NotImplementedError("Object save method not implemented")

    def delete(self, model_name, model_id):
        raise NotImplementedError("Object delete method not implemented")


class AWSEngine(Engine):
    def __init__(self, **kwargs):
        AWS_ACCESS_KEY_ID = kwargs.pop("AWS_ACCESS_KEY_ID")
        AWS_SECRET_ACCESS_KEY = kwargs.pop("AWS_SECRET_ACCESS_KEY")
        S3_BUCKET = kwargs.pop("S3_BUCKET")

        self.s3 = boto3.resource(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.bucket = self.s3.Bucket(S3_BUCKET)

    def save(self, model_name, model_id, file):
        self.delete(model_name, model_id)
        file_path = "%s_uploads/%s/%s" % (
            model_name,
            model_id,
            os.path.basename(file.name),
        )
        self.bucket.upload_file(file.name, file_path)

    def delete(self, model_name, model_id):
        folder_path = "%s_uploads/%s/" % (model_name, model_id)
        self.bucket.objects.filter(Prefix=folder_path).delete()
