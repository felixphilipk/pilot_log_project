from rest_framework import serializers
from .models import PilotLog

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """
    class Meta:
        model = PilotLog
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)


        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
