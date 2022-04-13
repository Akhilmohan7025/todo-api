from django.urls import path
from api import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('mytodos',views.Todosviewsets,basename='mytodos')
router.register('modeltodos',views.Todosmodelviewsets,basename='mytodosmodel')
router.register('signin',views.loginviews,basename='userlogin')
urlpatterns = [
    path('todos/', views.Todosview.as_view()),
    path('todos/<int:id>', views.Todosdetails.as_view()),
    path('mixins/todos/', views.todosmixinview.as_view()),
    path('mixins/todos/<int:id>', views.todomixinDetail.as_view()),
    path('account/signup/', views.usercreationview.as_view()),

]+router.urls
