# BellHop

BellHop is a simple way to upload files from Django applications. It is inspired by the [CarrierWave](https://github.com/carrierwaveuploader/carrierwave) gem for Ruby. Currently, only AWS is supported.

## Installation

Install from PyPI
```shell
pip install bellhop
```

Once done, add the `BELLHOP` settings in your `settings.py` file:
```python
BELLHOP = {
    "STORAGE": "aws",
    "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
    "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
    "S3_BUCKET": os.environ["S3_BUCKET"],
    "S3_REGION": os.environ["S3_REGION"],
}
```

## Example

Define a model in `models.py` which would store a file. The model should contain one `CharField` which we would use to reference the file.

In this example, the file would be stored using the field `file` of model `Document`.
```python
class Document(models.Model):
    file = models.CharField(max_length=255)
```

Create a file `uploaders.py` in your app. We would register the model with an uploader, where we define the field which references the file as `uploadable`, which is `file` in our case:
```python
from testapp.models import Document

from bellhop import bellhop, BaseUploader


class DocumentUploader(BaseUploader):
    uploadable = "file"


bellhop.register(Document, DocumentUploader)
```

Now, you can easily upload a file as:
```python
file = open('/path/to/file')
document = Document.objects.create(file=file)

# Access the url of the file
document.file_url
```