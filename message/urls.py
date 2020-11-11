from django.urls import path, re_path


from .views import ThreadView, InboxView, Inbox


urlpatterns = [
    path("inbox/", Inbox, name='inbox'),
    re_path(r"^(?P<username>[\w.@+-]+)/$", ThreadView.as_view(), name='thread'),
]