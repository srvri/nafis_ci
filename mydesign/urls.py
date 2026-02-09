# mydesign/urls.py
from django.urls import path
from . import views

app_name = "mydesign"

urlpatterns = [
    path("", views.mockup_page, name="mockup_page"),
    path("my-designs/", views.my_designs_page, name="my_designs_page"),
    path("edit/<int:design_id>/", views.edit_design_page, name="edit_design_page"),
    path("save/", views.save_design, name="save_design"),
    path("api/design/<int:design_id>/", views.get_design_api, name="get_design_api"),
    path("api/designs/", views.get_user_designs_api, name="get_user_designs_api"),
    path("result/<int:design_id>/", views.design_result, name="design_result"),
]
