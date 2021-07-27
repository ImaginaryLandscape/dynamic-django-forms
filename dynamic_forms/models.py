import json

from django.db import models
from .formfields import FormBuilderField, FormRenderField


class FormField(models.TextField):
    """Stores JSON Schema for form
    """
    # The methods 'from_db_value()', 'to_python()', and 'get_prep_value()'
    # had been removed in our version. I think this was due to a decision
    # to inherit from JSONField instead of TextField, as in the original.
    # But sadly this throws an error "__init__() got an unexpected keyword
    # argument 'encoder'" in modern Djangos, so I put them back - NTT.
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return []
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        if isinstance(value, str) or value is None:
            return value
        return json.dumps(value)

    def formfield(self, **kwargs):
        kwargs['form_class'] = FormBuilderField
        return super().formfield(**kwargs)


class ResponseField(models.TextField):
    """Stores JSON response to form.
    """

    # The same methods had been removed here as above; I'm putting
    # them back for the same reason - NTT

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return {}
        return json.loads(value)

    def get_prep_value(self, value):
        if isinstance(value, str) or value is None:
            return value
        # Datetime.date is not JSON serializable, so must specify to convert to string
        return json.dumps(value, default=str)

    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = FormRenderField
        return super().formfield(*args, **kwargs)
