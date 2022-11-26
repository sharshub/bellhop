import os
from io import IOBase

from django.db.models.query_utils import DeferredAttribute
from django.db.models.signals import pre_save, post_save, post_delete

from bellhop.engines import AWSEngine
from bellhop.uploaders import BaseUploader


class BellHop:
    def __init__(self):
        self._registry = {}
        self.engine = None

    def register(self, model, uploader):
        self._validate(model, uploader)
        self._registry[model] = uploader

        _uploadable_field_name = getattr(uploader, "uploadable")

        setattr(
            model,
            "%s_url" % (_uploadable_field_name),
            property(
                lambda instance: self.engine.object_url(
                    instance._meta.model.__name__.lower(),
                    instance.id,
                    getattr(instance, _uploadable_field_name),
                )
            ),
        )

        pre_save.connect(self.pre_save, sender=model, weak=False)
        post_save.connect(self.post_save, sender=model, weak=False)
        post_delete.connect(self.post_delete, sender=model, weak=False)

    def register_engine(self, **kwargs):
        storage = kwargs.pop("STORAGE")
        if not storage == "aws":
            raise Exception("Only AWS storage is supported")
        self.engine = AWSEngine(**kwargs)

    def pre_save(self, sender, **kwargs):
        instance = kwargs.get("instance")
        uploader = self._registry[sender]
        _uploadable_field_name = getattr(uploader, "uploadable")
        _uploadable_field_value = getattr(instance, _uploadable_field_name)

        if not instance.id:
            assert isinstance(
                _uploadable_field_value, IOBase
            ), "Cannot upload non-file object"

        if isinstance(_uploadable_field_value, IOBase):
            _file = _uploadable_field_value
            _file_name = os.path.basename(_file.name)

            setattr(instance, _uploadable_field_name, _file_name)
            setattr(instance, "bellhop_%s" % (_uploadable_field_name), _file)

    def post_save(self, sender, **kwargs):
        instance = kwargs.get("instance")
        uploader = self._registry[sender]
        _uploadable_field_name = getattr(uploader, "uploadable")

        if hasattr(instance, "bellhop_%s" % (_uploadable_field_name)):
            _id = instance.id
            _file = getattr(instance, "bellhop_%s" % (_uploadable_field_name))
            self.engine.save(
                model_name=sender.__name__.lower(),
                object_id=_id,
                file=_file,
            )

    def post_delete(self, sender, **kwargs):
        instance = kwargs.get("instance")

        self.engine.delete(
            model_name=sender.__name__.lower(),
            object_id=instance.id,
        )

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
