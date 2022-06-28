from django.urls import path, re_path
from . import views

app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("entry/<str:entry>", views.entry, name="url_entry"),
    re_path(r"search/$", views.search),
    path("newpage/", views.editpage, name="newpage"),
    path("editpage/", views.editpage, name="editpage"),
    path("editpage/<str:page_id>", views.editpage, name="editpage-arg")

]
