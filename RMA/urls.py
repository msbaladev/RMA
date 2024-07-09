from django.urls import path, include
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("dashboard/<str:quarter>/",dashboard,name="dashboard"),
    path("file-upload/<str:quarter>/",file_upload,name="file-upload"),
    path('download_Iness_rma_bulkapproval/<str:quarter>/',download_Iness_bulkapproval,name="download_Iness_rma_bulkapproval"),
    path('RMA_iness_bulk_upload/<str:quarter>/', RMA_iness_bulk_upload, name='RMA_iness_bulk_upload'),
]
