from django.conf import settings
from django.forms import TextInput
from tagging.fields import TagField
from tagging_ext.widgets import TagAutoCompleteInput

if "south" in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^tagging\_ext\.models\.TagAutocompleteField"])

class TagAutocompleteField(TagField):
    def formfield(self, **kwargs):
        defaults = {'widget': TagAutoCompleteInput}
        defaults.update(kwargs)
        return super(TagAutocompleteField, self).formfield(**defaults)
