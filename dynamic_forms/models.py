import datetime
import json
from django.contrib.postgres.fields import JSONField
from django.db import models
from .formfields import FormBuilderField, FormRenderField


class FormField(JSONField):

    def formfield(self, **kwargs):
        kwargs['form_class'] = FormBuilderField
        return super(FormField, self).formfield(**kwargs)


class ResponseField(JSONField):
    """Stores JSON response to form.
    """

    # def from_db_value(self, value, expression, connection, context):
    #     if value is None:
    #         return value
    #     bp()
    #     return json.loads(value)

    # def to_python(self, value):
    #     if isinstance(value, dict):
    #         return value
    #     if value is None:
    #         return {}
    #     return json.loads(value)

    # def get_prep_value(self, value):
    #     if isinstance(value, str) or value is None:
    #         return value
    #     # Datetime.date is not JSON serializable, so must specify to convert to string
    #     return json.dumps(value, default=str)

    def formfield(self, *args, **kwargs):
        kwargs['form_class'] = FormRenderField
        return super(ResponseField, self).formfield(*args, **kwargs)
