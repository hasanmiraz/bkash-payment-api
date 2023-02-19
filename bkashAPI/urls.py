from django.urls import path
from . import views

urlpatterns = [
    path("grant/",views.grantTokenView),
    path("refresh/",views.refreshTokenView),
    path("create/",views.createPaymentView),
    path("execute/",views.executePaymentView),
    path("refund/",views.refundView),
    path("cancelagreement/",views.cancelAgreementView),
    # path("",views.testing),
    path("",views.index),
]
