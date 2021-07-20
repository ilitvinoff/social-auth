from uuid import uuid4

from django.db import models
from django.utils.translation import gettext_lazy as _

class CoreModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4,editable=False)
    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("created"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("updated"))

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.pk)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.pk}>"