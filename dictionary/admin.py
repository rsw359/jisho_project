from django.contrib import admin
from .models import KanjiElement, ReadingElement, Sense, Entry

admin.site.register(KanjiElement)
admin.site.register(ReadingElement)
admin.site.register(Sense)
admin.site.register(Entry)



