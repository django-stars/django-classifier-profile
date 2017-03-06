from django.utils.functional import cached_property
from classifier.formsets import ClassifierFormSet

from .models import UserAttributeClassifier


class UserClassifierFormSet(ClassifierFormSet):
    """
    extended with one additional method to get forms grouped by category
    """

    @cached_property
    def grouped_forms(self):
        """
        grouped forms by category and filter options of kind field
        """
        self.empty_forms = {}
        forms = {}
        for kind in UserAttributeClassifier.objects.all():
            self.create_empty_form(kind)
            labels = list(kind.labels.values_list('pk', flat=True))
            forms[kind.category] = []
            for form in self.forms:
                label_id = None
                try:
                    label_id = form.cleaned_data['label'].pk
                except (AttributeError, KeyError):
                    label_id = form.data.get('label', form.initial.get('label'))

                if label_id in labels:
                    form.fields['label'].choices = kind.labels.values_list(
                        'pk', 'label'
                    )
                    forms[kind.category].append(form)

        return sorted(forms.items(), key=lambda i: i[0])

    def create_empty_form(self, kind):
        """
        returns empty form for specific attribute
        """
        form = self.form(
            auto_id=self.auto_id,
            prefix=self.add_prefix('__prefix__'),
            empty_permitted=True,
            use_required_attribute=False,
            **self.get_form_kwargs(None)
        )
        self.add_fields(form, None)
        form.fields['label'].choices = kind.labels.values_list('pk', 'label')
        form.fields['user'].initial = self.initial_extra[0]['user']

        self.empty_forms[kind.category] = form
