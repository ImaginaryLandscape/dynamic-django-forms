from django.views.generic.edit import FormMixin


class DynamicFormMixin(FormMixin):
    form_model_pk_field = None
    form_field = "form"
    form_pk_url_kwarg = "pk"

    response_form_fk_field = None
    response_field = "response"

    def _get_object_containing_form(self, pk):
        return self.form_model.objects.get(pk=pk)

    def get_form(self, *args, **kwargs):
        form = super(DynamicFormMixin, self).get_form(*args, **kwargs)
        # Get instance of model containing form used for this response. Save this object as an instance variable for use in form_valid method
        form_instance_pk = self.kwargs[self.form_pk_url_kwarg]
        self.form_instance = self._get_object_containing_form(form_instance_pk)
        # Get json form configuration from form-containing object
        json_data = getattr(self.form_instance, self.form_field)
        # Add fields in JSON to dynamic form rendering field.
        form.fields[self.response_field].add_fields(json_data, form)
        return form
