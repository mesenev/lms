from group.models import CourseGroup
from rest_framework import serializers
from users.models import GroupAssignTeacher
from group.models import CourseGroupLink
import random
import string


class CourseGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseGroup
        fields = '__all__'

    def create(self, validated_data):
        instanse = CourseGroup.objects.create(**validated_data)
        request = self.context.get("request")
        user = request.user
        assign_teacher = GroupAssignTeacher(user=user, group=instanse)
        assign_teacher.save()
        return instanse


class CourseGroupLinkSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    group = serializers.PrimaryKeyRelatedField(queryset=CourseGroup.objects.all())
    link = serializers.SerializerMethodField(required=False)
    usages = serializers.IntegerField()

    @staticmethod
    def get_link(instance):
        return instance.link

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        return CourseGroupLink.objects.create(**validated_data, link=''.join(
            random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(15)))

    class Meta:
        model = CourseGroupLink
        fields = '__all__'
