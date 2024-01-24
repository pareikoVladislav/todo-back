from django.urls import path

from apps.category.views import (
    CategoryListGenericView,
    RetrieveCategoryGenericView
)


urlpatterns = [
    path("", CategoryListGenericView.as_view()),
    path("<int:category_id>/", RetrieveCategoryGenericView.as_view()),
]
