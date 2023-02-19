from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import refundModel, grantTokenModel, createPaymentIDModel, successPaymentModel, agreementModel
from django.shortcuts import redirect

import requests
import environ
env = environ.Env()
environ.Env.read_env("paymentIntegrationBkash\.env")

from . import requestData 

# debuging
def debugTool(**kwargs):
    print("-"*30)
    for key, value in kwargs.items():
        print(f"task = {key}, taskResult = {value}\n")
    print("-"*30)

# Create your views here.

#Index Page
@api_view(["GET"])
def index(request):
    agreementModel_query = agreementModel.objects.all()
    json_responseApi = requestData.indexData(agreementModel_query)
    if request.method == "GET":
        return render(request, "index.html", json_responseApi)

# GRANT TOKEN
@api_view(["GET"])
def grantTokenView(request):
    if request.method == "GET":
        grantTokenModel_query = grantTokenModel.objects.all()
        grantTokenModel_object = grantTokenModel()
        
        [url, payload, headers]= requestData.grantTokenData()

        responseApi = requests.post(url, json=payload, headers=headers)
        json_responseApi = responseApi.json()

        grantTokenModel_object.id_token = json_responseApi["id_token"]
        grantTokenModel_object.refresh_token = json_responseApi["refresh_token"]
        
        if len(grantTokenModel_query)!=0:
            grantTokenModel_object.id = grantTokenModel_query[0].id
            
        grantTokenModel_object.save()

        debugTool(function_name = "grantTokenView", query = grantTokenModel_query, url = url, payload = payload, headers = headers, json_responseApi = json_responseApi, request_mode = request.GET.get('mode'))

        return redirect("http://127.0.0.1:8000/create/?mode="+str(request.GET.get('mode')))
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# REFRESH TOKEN
@api_view(["GET"])
def refreshTokenView(request):
    if request.method == "GET":
        debugTool()
        return Response(status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Create Payment and Create Agreement
@api_view(["GET"])
def createPaymentView(request):
    if request.method == "GET":
        grantTokenModel_query = grantTokenModel.objects.get()
        createPaymentIDModel_object = createPaymentIDModel()
        
        mode = request.GET.get("mode")
        
        if(mode == "0011"):
            [url, payload, headers]= requestData.createPaymentData(grantTokenModel_query.id_token)      
            responseApi = requests.post(url, json=payload, headers=headers)

        elif(mode == "0000"):
            [url, payload, headers]= requestData.createAgreementData(grantTokenModel_query.id_token)      
            responseApi = requests.post(url, json=payload, headers=headers)
        
        elif(mode == "0001"):
            agreementModel_query = agreementModel.objects.get()
            [url, payload, headers]= requestData.createPaymentWithAgreementData(grantTokenModel_query.id_token, agreementModel_query.agreementID)      
            responseApi = requests.post(url, json=payload, headers=headers)
        
        else:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

        json_responseApi = responseApi.json()
        createPaymentIDModel_object.paymentID = json_responseApi["paymentID"]
        createPaymentIDModel_object.save()

        debugTool(function_name = "createPaymentView", json_responseApi = json_responseApi, request_mode = request.GET.get("mode"))

        return redirect(json_responseApi["bkashURL"])
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Execute Payment and Execute Agreement
@api_view(["GET"])
def executePaymentView(request):
    if request.method == "GET":
        grantTokenModel_query = grantTokenModel.objects.get()
        successPaymentModel_object = successPaymentModel()
        agreementModel_object = agreementModel()

        get_paymentID = request.GET.get("paymentID")
        get_status = request.GET.get("status")

        [url, payload, headers]= requestData.executeData(get_paymentID, grantTokenModel_query.id_token)      
        responseApi = requests.post(url, json=payload, headers=headers)
        json_responseApi = responseApi.json()

        if get_status == "success":
            debugTool(function_name = "executePaymentView", json_responseApi = json_responseApi)
            if json_responseApi["statusMessage"] != "Successful":
                json_responseApi = requestData.statusData(json_responseApi["statusMessage"], get_paymentID, "")

            # for payment execution
            elif "trxID" in json_responseApi:
                successPaymentModel_object.paymentID = request.GET.get("paymentID")
                successPaymentModel_object.trxID = json_responseApi["trxID"]
                successPaymentModel_object.save()
                json_responseApi = requestData.statusData(json_responseApi["statusMessage"], get_paymentID, successPaymentModel_object.trxID)

            # for agreement execution
            elif "agreementID" in json_responseApi:
                agreementModel_object.agreementID = json_responseApi["agreementID"]
                agreementModel_object.save()
                json_responseApi = requestData.agreementStatusData(json_responseApi["statusMessage"], get_paymentID, json_responseApi["agreementID"])

            else:
                return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)    

        else:
            json_responseApi = requestData.statusData(get_status, get_paymentID, "")

        debugTool(function_name = "executePaymentView", get_paymentID = get_paymentID, get_status = get_status, json_responseApi = json_responseApi, trxID = successPaymentModel_object.trxID, responseApi = responseApi.json())

        return render(request, "status.html", json_responseApi)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

# Cancel Agreement
@api_view(["GET"])
def cancelAgreementView(request):
    if request.method == "GET":
        grantTokenModel_query = grantTokenModel.objects.get()
        agreementModel_query = agreementModel.objects.get()
        
        [url, payload, headers] = requestData.cancelAgreementData(grantTokenModel_query.id_token, agreementModel_query.agreementID)      
        responseApi = requests.post(url, json=payload, headers=headers)
        json_responseApi = responseApi.json()
        
        debugTool(function_name = "cancelAgreementView", aggreementID = agreementModel_query.agreementID, responseApi = responseApi)

        if json_responseApi["statusMessage"] == "Successful":
            agreementModel.objects.all().delete()
            return render(request, "status.html", json_responseApi)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

# REFUND
@api_view(["GET", "POST"])
def refundView(request):
    if request.method == "GET":
        return render(request, "refund.html")
    
    elif request.method == "POST":
        grantTokenModel_query = grantTokenModel.objects.get()
        refundModel_object = refundModel()

        paymentID = request.POST.get("paymentID")
        trxID = request.POST.get("trxID")

        [url, payload, headers] = requestData.refundData(grantTokenModel_query.id_token, paymentID, trxID)      
        responseApi = requests.post(url, json=payload, headers=headers)
        json_responseApi = responseApi.json()
        debugTool(function_name = "refundView", json_responseApi = json_responseApi, paymentID = paymentID, trxID = trxID)
        
        refundModel_object.paymentID = paymentID
        refundModel_object.trxID = json_responseApi["originalTrxID"]
        refundModel_object.refundTrxID = json_responseApi["refundTrxID"]
        
        refundModel_object.save()

        debugTool(function_name = "refundView", paymentID = paymentID, trxID = trxID, json_responseApi = json_responseApi)
        return render(request, "status.html", json_responseApi)
    
    else:
        return Response(status = status.HTTP_400_BAD_REQUEST)
        

        