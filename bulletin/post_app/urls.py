from django.urls import path

from .views import change_status, PostList, PostCreate, PostDetail, PostDelete, PostUpdate, UserPost, ReplyCreate, \
    UserReplies, ReplyDelete, subscribe

urlpatterns = [

    path('list/', PostList.as_view(), name='posts'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/detail/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('userlist/', UserPost.as_view(), name='userlist'),
    path('<int:pk>/detail/replycreate', ReplyCreate.as_view(), name='replycreate'),
    path('userreplies/', UserReplies.as_view(), name='userreplies'),
    path('userreplies/change_status', change_status, name='change_status'),
    path('userreplies/<int:pk>/delete_reply', ReplyDelete.as_view(), name='delete_reply'),
    path('subscribe/', subscribe, name='subscribe'),

]
