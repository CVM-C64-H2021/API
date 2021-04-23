from django.db import models

class Sii_Api(models.Model):
    # Id sera automatique
    m_idApp = models.IntegerField(blank=False, default='')
    m_date = models.DateField()
    m_type = models.CharField(max_length=70, blank=False, default='')
    m_valeur = models.CharField(max_length=200,blank=False, default='')
    m_alerte = models.BooleanField(default=False)
    m_message = models.CharField(max_length=255,blank=True, default='')

class User(models.Model):
    username = models.CharField(max_length=70, blank=False, default='')
    password = models.CharField(max_length=200,blank=False, default='')