from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from classifier.models import ClassifierAbstract, ClassifierLabelAbstract

from .managers import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)

    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ('first_name', 'last_name', )

    def __str__(self):
        return self.get_full_name()

    def get_short_name(self):
        if self.first_name:
            return self.first_name
        return self.email.split('@')[0]

    def get_full_name(self):
        return ' '.join(filter(None, [self.first_name, self.last_name]))

    def get_mobile(self):
        attr = (
            self.attributes
            .filter(label__slug=UserAttributeClassifierLabel.PHONE_MOBILE)
            .first()
        )
        if attr:
            return attr.value

    def get_skype(self):
        attr = (
            self.attributes
            .filter(label__slug=UserAttributeClassifierLabel.IM_SKYPE)
            .first()
        )
        if attr:
            return attr.value

    def get_birhday(self):
        attr = (
            self.attributes
            .filter(label__slug=UserAttributeClassifierLabel.GENERAL_BIRTHDAY)
            .first()
        )
        if attr:
            return attr.label.classifier.to_python(attr.value)


class UserAttributeClassifier(ClassifierAbstract):
    category = models.CharField(max_length=100)

    class Meta:
        ordering = ('category', )


class UserAttributeClassifierLabel(ClassifierLabelAbstract):
    # have to be the same as in database to be able to fetch specific value
    GENERAL_BIRTHDAY = 'birthday'
    PHONE_MOBILE = 'mobile'
    IM_SKYPE = 'skype'

    classifier = models.ForeignKey(
        UserAttributeClassifier,
        related_name='labels'
    )
    slug = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        ordering = ('label', )


class UserAttribute(models.Model):
    user = models.ForeignKey(User, related_name='attributes')
    label = models.ForeignKey(UserAttributeClassifierLabel, related_name='+')
    value = models.CharField(max_length=200)
