from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from links.models import Link

# Create your views here.
class NewCreateView(CreateView):
    model = Link
    fields = (
        'title', 'url'
    )

    template_name = 'links/new.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NewCreateView, self).dispatch(*args,**kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewCreateView, self).get_context_data(**kwargs)
        context['section'] = 'links'
        return context

    def form_valid(self, form):
        new_link = form.save(commit=False)
        new_link.submitter = self.request.user
        new_link.save()

        self.object = new_link

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        return reverse('links')
