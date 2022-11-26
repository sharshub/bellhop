from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import pre_save, post_save, post_delete

from bellhop.uploaders import BaseUploader


class BellHop:
    def __init__(self):
        self._registry = {}

    def register(self, model, uploader):
        self._validate(model, uploader)
        self._registry[model] = uploader

        pre_save.connect(self.pre_save, sender=model, weak=False)
        post_save.connect(self.post_save, sender=model, weak=False)
        post_delete.connect(self.post_delete, sender=model, weak=False)

    def pre_save(self, sender, **kwargs):
        print("pre save signal received")
        pass

    def post_save(self, sender, **kwargs):
        print("post save signal received")
        pass

    def post_delete(self, sender, **kwargs):
        print("post delete signal received")
        pass

    def _validate(self, model, uploader):
        assert (
            isinstance(uploader, type) and uploader.__base__ == BaseUploader
        ), "uploader should be a subclass of BaseUploader"

        _uploadable_field_name = getattr(uploader, "uploadable")

        assert hasattr(
            model, _uploadable_field_name
        ), "%s does not have the uploadable field %s defined" % (
            model.__name__,
            _uploadable_field_name,
        )

        _uploadable_field = getattr(model, _uploadable_field_name)

        assert isinstance(
            _uploadable_field, DeferredAttribute
        ), "'%s' in model %s should be a database field" % (
            _uploadable_field_name,
            model.__name__,
        )


bellhop = BellHop()
