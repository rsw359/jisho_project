from django.db import models

class KanjiElement(models.Model):
  keb = models.CharField(max_length=255)
  ke_inf = models.TextField(null=True, blank=True)
  ke_pri = models.TextField(null=True, blank=True)

class ReadingElement(models.Model):
  reb = models.CharField(max_length=255)
  re_nokanji = models.BooleanField(default=False)  
  re_refr = models.TextField(null=True, blank=True)
  re_inf = models.TextField(null=True, blank=True)
  re_pri = models.TextField(null=True, blank=True)

class Sense(models.Model):
  gloss = models.TextField()
  pos = models.TextField(null=True, blank=True)
  xref = models.TextField(null=True, blank=True)
  ant = models.TextField(null=True, blank=True)
  field = models.TextField(null=True, blank=True)
  lsource = models.TextField(null=True, blank=True)
  misc = models.TextField(null=True, blank=True)
  example = models.TextField(null=True, blank=True)


class Entry(models.Model):
  ent_seq = models.IntegerField(unique=True)
  keb_elem = models.ManyToManyField(KanjiElement, blank=True)
  reb_elem = models.ManyToManyField(ReadingElement)
  sense = models.ManyToManyField(Sense)