from django.core.urlresolvers import reverse
from django.forms import modelformset_factory
from django.http import HttpResponseForbidden
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from .models import User, UserAttribute
from .formsets import UserClassifierFormSet
from .forms import UserForm, UserAttributeForm


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'account/profile_edit.html'

    def get_object(self, queryset=None):
        if (
            not self.kwargs.get(self.pk_url_kwarg)
            and not self.kwargs.get(self.slug_url_kwarg)
        ):
            self.kwargs[self.pk_url_kwarg] = self.request.user.pk

        user = super(ProfileEditView, self).get_object(queryset=queryset)

        if user != self.request.user and not self.request.user.is_superuser:
            raise HttpResponseForbidden

        return user

    def get_context_data(self, **kwargs):
        context = super(ProfileEditView, self).get_context_data(**kwargs)

        if not context.get('attribute_formset'):
            context['attribute_formset'] = self.get_formset()

        return context

    def form_valid(self, form):
        formset = self.get_formset()
        if formset.is_valid():
            form.save()
            formset.save()
        else:
            return self.form_invalid(form, attribute_formset=formset)

        return redirect(reverse('profile-edit'))

    def form_invalid(self, form, attribute_formset=None):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                attribute_formset=attribute_formset
            )
        )

    def get_formset(self):
        """
        create formset of attributes with help of custome formset class
        """
        FormSetClass = modelformset_factory(
            UserAttribute,
            formset=UserClassifierFormSet,
            form=UserAttributeForm,
            can_delete=True,
            extra=0
        )

        formset = FormSetClass(
            data=self.request.POST if self.request.method == 'POST' else None,
            queryset=self.get_object().attributes.all(),
            initial={
                'user': self.get_object().pk,
            }
        )

        return formset
