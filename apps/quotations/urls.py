from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index, name="main"),
    url(r'^register$', views.register, name="create_user"),
    url(r'^login$', views.login, name="login_user"),
    url(r'^quotes$', views.quotes, name="quotes"),
    url(r'^add$', views.add, name="add"),
    url(r'^favorite/(?P<quote_id>\d+)$', views.favorite, name="favorite"),
    url(r'^unfavorite/(?P<quote_id>\d+)$', views.unfavorite, name="unfavorite"),
    url(r'^users/(?P<user_id>\d+)$', views.userpage, name="userpage"),
    url(r'^logout$', views.logout, name="logout")
]
