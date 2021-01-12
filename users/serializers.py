from rest_framework import serializers

from users.models import User


class DefaultUserSerializer(serializers.ModelSerializer):
    staff_for = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    def __init__(self, *args, exclude_staff=True, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if exclude_staff:
            self.fields.pop('staff_for')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'id', 'staff_for']
