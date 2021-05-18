from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('signin', views.signin),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('register', views.register),
    path('add_pet', views.add_pet),
    path('newpet', views.newpet),
    path('pets/<int:id>', views.pet),
    path('pets/edit/<int:id>', views.edit_form),
    path('edit_pet/<int:id>', views.edit_pet),
    path('delete_pet/<int:id>', views.delete_pet),
    path('favorite/<int:id>', views.favorite),
    path('account', views.account),
    path('pets/adopt/<int:id>', views.adopt_form),
    path('adopt_pet/<int:id>', views.adopt_pet),

]