from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Entry
from django.db import models

class SearchView(TemplateView):
  template_name = 'dictionary/search.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    query = self.request.GET.get('q')
    if query:
       #search across kanji, gloss, and readings fields
       results = Entry.objects.filter(
         models.Q(keb_elem__keb_icontains=query) |
         models.Q(reb_elem__reb_icontains=query) |
         models.Q(sense__gloss__icontains=query)
         ).distinct()
    else:
      results = None

    context['results'] = results
    context['query'] = query

    return context
