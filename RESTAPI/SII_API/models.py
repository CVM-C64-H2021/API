from django.db import models

class Sii_Api(models.Model):
    # Id sera automatique
    m_date = models.DateTimeField(auto_now_add=True, null=True)
    m_type = models.CharField(max_length=70, blank=False, default='')
    m_value = models.CharField(max_length=200,blank=False, default='')
    m_alert = models.BooleanField(default=False)
    m_msg = models.CharField(max_length=255,blank=True, default='')