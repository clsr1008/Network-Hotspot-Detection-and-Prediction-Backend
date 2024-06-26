from django.urls import path
from users.views import LoginView, UserInfoView, LogoutView, getHotspotsView, getCategoryView, getWordFrequencyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('info/', UserInfoView.as_view(), name='user_info'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('getHotspots/', getHotspotsView.as_view(), name='getHotspots'),
    path('getCategory/', getCategoryView.as_view(), name='getCategory'),
    path('getWordFrequency/', getWordFrequencyView.as_view(), name='getWordFrequency'),
]