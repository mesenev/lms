import json

from django.shortcuts import render

from users.models import User
from users.serializers import DefaultUserSerializer


# @login_required(login_url=reverse_lazy('account_login'))
def index(request, *args, **kwargs):
    user = User.objects.get(pk=request.user.id)
    user_data = json.dumps(DefaultUserSerializer(instance=user).data)
    return render(request, 'index.html', context=dict(user_data=user_data))
