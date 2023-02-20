from django.urls import path
from . import views

urlpatterns = [
    path("grant/",views.grantTokenView),
    path("refresh/",views.refreshTokenView),
    path("create/",views.createView),
    path("execute/",views.executeView),
    path("refund/",views.refundView),
    path("cancelagreement/",views.cancelAgreementView),
    # path("test",views.testView),
    path("",views.index),
]
