from group.models import Group
from rest_framework import serializers
from users.models import GroupAssignTeacher
from group.models import GroupLink
import random
import string

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = '__all__'

    def create(self, validated_data):
        instanse = Group.objects.create(**validated_data)
        request = self.context.get("request")
        user = request.user
        assign_teacher = GroupAssignTeacher(user=user, group=instanse)
        assign_teacher.save()
        return instanse


class LinkSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    link = serializers.SerializerMethodField(required=False)
    usages = serializers.IntegerField()

    @staticmethod
    def get_link(instance):
        return instance.link

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return GroupLink.objects.create(**validated_data, link=''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(15)))

    class Meta:
        model = GroupLink
        fields = '__all__'
