from django.db.models import (
    Model, CharField, PositiveIntegerField, TextField, ForeignKey
)
from django.utils.translation import ugettext_lazy as _

from model_utils import Choices


class Version(Model):
    name = CharField(max_length=255)
    tag = CharField(max_length=255)

    def __str__(self):
        return self.name


class Module(Model):
    filename = CharField(max_length=255)
    path = CharField(max_length=255)
    version = ForeignKey(Version, related_name="modules")

    def get_full_path(self):
        if self.filename == "__init__.py":
            return "%s/%s" % (self.path.replace(".", "/"), self.filename)
        else:
            return "%s.py" % self.path.replace(".", "/")


class Object(Model):
    TYPES = Choices(
        ("c", "class", _("class")),
        ("f", "function", _("function")),
        ("u", "unknown", _("unknown"))
    )

    name = CharField(max_length=255)
    module = ForeignKey(Module)
    short_import = CharField(max_length=255)
    docstring = TextField()
    code = TextField()
    line = PositiveIntegerField()
    type = CharField(choices=TYPES, max_length=1)

    def get_github_url(self):
        return "https://github.com/django/django/tree/%s/%s#L%s" % (
            self.module.version.tag, self.module.get_full_path(), self.line
        )
