from django.db.models import fields
from rest_framework import serializers
from SII_API.models import Sii_Api

class ApiSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sii_Api
        fields = (  'm_idApp',
                    'm_date',
                    'm_type',
                    'm_valeur',
                    'm_alerte',
                    'm_message', )