from django import template
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe


class TagAutoCompleteInput(forms.TextInput):
    
    class Media:
        css = {
            "all": (settings.STATIC_URL + "pinax/css/jquery.autocomplete.css",)
        }
        js = (
            settings.STATIC_URL + "pinax/js/jquery-1.3.2.min.js",
            settings.STATIC_URL + "pinax/js/jquery.bgiframe.min.js",
            settings.STATIC_URL + "pinax/js/jquery.ajaxQueue.js",
            settings.STATIC_URL + "pinax/js/jquery.autocomplete.min.js"
        )
    
    def init(self, *args, **kwargs):
        if len(args) == 4:
            self.app_label = args[0]
            self.model = args[1]
            args = args[2:]
            super(TagAutoCompleteInput, self).__init__(*args, **kwargs)
        else:
            super(TagAutoCompleteInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        output = super(TagAutoCompleteInput, self).render(name, value, attrs)
        
        return output + mark_safe(u"""
            <script type="text/javascript">
                $(function() {
                    $("#id_%s").autocomplete({
                        source: function(request, response) {
                            $.getJSON("%s", {
                                term: request.term.split(" ").pop(),
                            }, response);
                        },
                        focus: function() { return false; },
                        select: function(event, ui) {
                            var separator = " ";
                            if(this.value.search(",") != -1)
                                separator = ",";

                            var terms = this.value.split(separator);
                            terms.pop();
                            terms.push($.trim(ui.item.value));
                            terms.push("");
                            this.value = terms.join(", ");
                            return false;
                        },
                    })
                });
            </script>""" % (
                name,
                reverse("tagging_ext_autocomplete", kwargs={
                    "app_label": self.app_label,
                    "model": self.model }
                        if 'app_label' in self.__dict__ else {}
                )
            )
        )
