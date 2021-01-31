from rest_framework import serializers

from users.models import User


class DefaultUserSerializer(serializers.ModelSerializer):
    staff_for = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    def __init__(self, *args, exclude_staff=True, **kwargs):
        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)
        if exclude_staff:
            self.fields.pop('staff_for')

    def create(self, validated_data):
        password = validated_data['password']
        del validated_data['password']
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'id', 'staff_for', 'password', 'email', 'avatar_url']
        # 'get_avatar']
        extra_kwargs = {'password': {'write_only': True}}
        # read_only_fields = ['get_avatar']
