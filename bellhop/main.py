from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import post_save, post_delete

from bellhop.uploaders import BaseUploader


class BellHop:
    REGISTERED_MODELS = dict()

    @classmethod
    def register(cls, model):
        uploader = cls._validate(model)
        cls.REGISTERED_MODELS[model] = uploader
        post_save.connect(cls.post_save, sender=model, weak=False)
        post_delete.connect(cls.post_delete, sender=model, weak=False)

    @classmethod
    def post_save(cls, sender, **kwargs):
        print("post save signal received")
        pass

    @classmethod
    def post_delete(cls, sender, **kwargs):
        print("post delete signal received")
        pass

    @classmethod
    def _validate(cls, model):
        uploader = getattr(model, "mount_uploader")

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

        return uploader
