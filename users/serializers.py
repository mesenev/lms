from rest_framework import serializers

from users.models import User, StudyGroup


class StudyGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGroup
        fields = ['study_group']


class DefaultUserSerializer(serializers.ModelSerializer):
    study_group = serializers.CharField(max_length=20)
    staff_for = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)

    def __init__(self, *args, exclude_staff=False, **kwargs):
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

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar_url = validated_data.get('avatar_url', instance.avatar_url)
        instance.username = validated_data.get('username', instance.username)
        password = validated_data['password']
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'study_group', 'id', 'staff_for', 'password',
                  'email', 'avatar_url', 'thumbnail', 'middle_name', 'cats_account']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['thumbnail']
