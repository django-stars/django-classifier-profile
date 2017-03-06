from django import forms
from classifier.forms import ClassifierFormMixin

from django_classifier_profile.utils.forms import BootstrapFormMixin
from .models import User, UserAttribute


class UserForm(BootstrapFormMixin, forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name', 'last_name',
        )


class UserAttributeForm(
    BootstrapFormMixin, ClassifierFormMixin, forms.ModelForm
):
    CLASSIFIER_VALUE_FIELD = 'value'

    class Meta:
        model = UserAttribute
        fields = (
            'id', 'user', 'label', 'value',
        )
