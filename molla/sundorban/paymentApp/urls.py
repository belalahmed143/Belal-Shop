from django.urls import path
from .views import *

urlpatterns = [
    path("checkout/",CheckOutView.as_view(), name="Check-Out"),
    path("sslc/statuse/", sslc_status, name="status"),
    path("sslc/complete/<val_id>/<tran_id>/", sslc_complete, name="sslc-complete"),
]
