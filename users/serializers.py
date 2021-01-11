from rest_framework import serializers

from users.models import User, CourseAssign


class DefaultUserSerializer(serializers.ModelSerializer):
    staff_for = serializers.SerializerMethodField()

    def get_staff_for(self, obj):
        return list(CourseAssign.objects.filter(is_staff=True, user=obj).values_list('id', flat=True))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'id', 'staff_for']
