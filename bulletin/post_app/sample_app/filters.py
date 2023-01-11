from django_filters import FilterSet
from ..models import Reply


class ReplyFilter(FilterSet):
    class Meta:
        model = Reply
        fields = {
            'user__username': ['exact'],
            'post__title': ['exact'],
            'date': ['lt', 'gt'],
            'content': ['icontains'],
            'status': ['exact'],
        }