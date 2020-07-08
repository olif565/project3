"""ProjectSkripsi URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from home.views import view_data_training, view_data_testing, view_normalisasi, view_training, view_diagnosis, \
    view_kernel, view_data_user, view_testing_2, view_testing_1

app_name = 'home'

urlpatterns = [
    path('', view_data_training.dashboard, name='index'),
    path('data-user', view_data_user.IndexView.as_view(), name='data-user'),
    path('data-training', view_data_training.IndexView.as_view(), name='data-training'),
    path('data-testing', view_data_testing.IndexView.as_view(), name='data-testing'),

    path('detail-user/<int:pk>/', view_data_user.detail, name='detail-user'),
    path('detail-training/<int:pk>/', view_data_training.DataDetailView.as_view(), name='detail-training'),
    path('detail-testing/<int:pk>/', view_data_testing.DataDetailView.as_view(), name='detail-testing'),
    
    path('edit-user/<int:pk>/', view_data_user.edit, name='edit-user'),
    path('edit-training/<int:pk>/', view_data_training.edit, name='edit-training'),
    path('edit-testing/<int:pk>/', view_data_testing.edit, name='edit-testing'),
    
    path('create-user/', view_data_user.create, name='create-user'),
    path('create-training/', view_data_training.create, name='create-training'),
    path('create-testing/', view_data_testing.create, name='create-testing'),
   
    path('delete-user/<int:pk>/', view_data_user.delete, name='delete-user'),
    path('delete-training/<int:pk>/', view_data_training.delete, name='delete-training'),
    path('delete-testing/<int:pk>/', view_data_testing.delete, name='delete-testing'),

    path('normalisasi/<int:level>/', view_normalisasi.IndexView.as_view(), name='normalisasi'),
    path('kernel/<int:level>/', view_kernel.IndexView.as_view(), name='kernel'),
    path('training/<int:level>/', view_training.IndexView.as_view(), name='training'),

    path('diagnosis', view_diagnosis.IndexView.as_view(), name='diagnosis'),
    path('diagnosis_normalisasi', view_diagnosis.NormalisasiView.as_view(), name='diagnosis_normalisasi'),
    path('diagnosis_kernel', view_diagnosis.KernelView.as_view(), name='diagnosis_kernel'),

    path('testing_manual', view_testing_1.IndexView.as_view(), name='testing_manual'),
    path('testing_svm', view_testing_2.IndexView.as_view(), name='testing_svm'),

    path('logout', view_data_training.logout_view, name='logout')
]
