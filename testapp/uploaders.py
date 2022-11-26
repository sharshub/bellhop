from testapp.models import Document

from bellhop import bellhop, BaseUploader


class DocumentUploader(BaseUploader):
    uploadable = "file"


bellhop.register(Document, DocumentUploader)
