class BaseUploaderMeta(type):
    def __new__(cls, name, bases, attrs):
        return super().__new__(cls, name, bases, attrs)


class BaseUploader(metaclass=BaseUploaderMeta):
    uploadable = "file"
