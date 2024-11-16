# users/urls.py
from django.urls import path
from .views import LoadUserDataView, SearchUserView

urlpatterns = [
    path('load-user-data/', LoadUserDataView.as_view(), name='load_user_data'),
    path('search-user/', SearchUserView.as_view(), name='search_user'),
]
