from django.urls import path
from . import views
from .views import TestCreateView, FavoriteCourseView, MyCourseView, AddCourseToMyCourse

app_name = "api"

urlpatterns = [
    path('sign-up/', views.UserRegistrationView.as_view(), name='register'),
    path('accounts/profile/', views.UserProfileView.as_view(), name='profile'),
    path('chat/', views.ChatQueryView.as_view()),
    path('chat/history/', views.ChatHistoryAll.as_view()),
    path('chat/history/<int:pk>/delete/', views.ChatHistoryDetailDelete.as_view()),
    path('test/', TestCreateView.as_view(), name='create-test'),
    path('test/my-tests/', views.TestAll.as_view(), name='all_tests'),
    path('test/my-tests/<int:pk>/detail/', views.TestDeleteView.as_view(), name='delete_test'),
    path("courses/", views.CoursesListView.as_view(),name="courses"),
    path("courses/upload/", views.CourseQueryView.as_view()),
    path("courses/<int:pk>/detail/", views.CourseDetailView.as_view()),
    path("courses/<int:pk>/videos/", views.CourseVideosView.as_view(),name="videos"),
    path("courses/<int:pk>/videos/post-video/", views.CourseVideoQueryView.as_view()),
    path("courses/<int:pk>/videos/<int:video_id>/", views.CourseVideoDetail.as_view()),
    path("courses/<int:pk>/videos/<int:video_id>/delete/",views.CourseVideoDeleteView.as_view()),
    path("courses/<int:pk>/videos/<int:video_id>/update/", views.CourseVideoUpdateView.as_view()),
    path("courses/purchases/",views.PayCourseView.as_view(),name="purchases"),
    path("courses/purchases/<int:purchase_id>/access/", views.access_view, name='access_view'),
    path("courses/<int:pk>/shop/", views.PayCourseQueryView.as_view()),
    path('favorites/', FavoriteCourseView.as_view(), name='favorite-course-list'),
    path('favorites/<int:pk>/', views.FavoriteCourseDeleteView.as_view(), name='favorite-delete'),
    path('add-courses/', AddCourseToMyCourse.as_view(), name='add_courses'),
    path('my-courses/', MyCourseView.as_view(), name='my-course-list'),
    path('my-courses/<int:pk>/', views.FavoriteCourseDeleteView.as_view(), name='my-course-delete'),

]
