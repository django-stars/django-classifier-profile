from django.contrib import admin
from django.db.utils import OperationalError

from .models import (
    User, UserAttributeClassifier, UserAttributeClassifierLabel, UserAttribute
)


class BaseUserAttributeAdmin(admin.TabularInline):
    model = UserAttribute
    extra = 0

    def get_queryset(self, request):
        qs = super(BaseUserAttributeAdmin, self).get_queryset(request)
        label_model = self.model._meta.get_field('label').related_model
        classifier_field_name = label_model.get_classifier_related_field().name
        kwargs = {
            'label__{}'.format(classifier_field_name): self.CLASSIFIER,
        }
        qs = qs.filter(**kwargs)

        return qs


def user_attribute_admin_factory(classifier):
    class UserAttributeAdmin(BaseUserAttributeAdmin):
        CLASSIFIER = classifier
        verbose_name = classifier.category
        verbose_name_plural = classifier.category

    return UserAttributeAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', )

    @property
    def inlines(self):
        inlines = []
        try:
            for classifier in UserAttributeClassifier.objects.all():
                inline_cls = user_attribute_admin_factory(classifier)
                inlines.append(inline_cls)
        except OperationalError: # raised when migrations weren't applied
            pass

        return inlines


class UserAttributeClassifierLabelAdmin(admin.TabularInline):
    model = UserAttributeClassifierLabel


@admin.register(UserAttributeClassifier)
class UserAttributeClassifierAdmin(admin.ModelAdmin):
    list_display = (
        'kind', 'category', 'labels', 'value_type', 'value_validator'
    )
    inlines = [
        UserAttributeClassifierLabelAdmin,
    ]

    def labels(self, obj):
        return ', '.join(obj.labels.values_list('label', flat=True))
