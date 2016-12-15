from django.forms import Form, CharField, ModelChoiceField, Select, TextInput
from django.utils.translation import ugettext_lazy as _

from dilu.models import Version


class SearchForm(Form):
    query = CharField(
        min_length=3,
        widget=TextInput(attrs={'class': "form-control",
                                'placeholder': _("Class or function")})
    )
    version = ModelChoiceField(
        queryset=Version.objects.all(),
        widget=Select(attrs={'class': "form-control"}),
        to_field_name="tag",
        empty_label=None,
    )
