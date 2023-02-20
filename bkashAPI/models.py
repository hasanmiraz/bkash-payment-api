from django.db import models

# Create your models here.

class grantTokenModel(models.Model):
    id_token = models.TextField()
    refresh_token = models.TextField()

class createPaymentIDModel(models.Model):
    paymentID = models.TextField()

class successPaymentModel(models.Model):
    paymentID = models.TextField()
    trxID = models.TextField()

class agreementModel(models.Model):
    agreementID = models.TextField()
    customerMsisdn = models.TextField()

class refundModel(models.Model):
    paymentID = models.TextField()
    trxID = models.TextField()
    refundTrxID = models.TextField()