import environ
env = environ.Env()
environ.Env.read_env("paymentIntegrationBkash\.env")

def getHeaders(id_token):
    headers = {
                "accept": "application/json",
                "Authorization": id_token,
                "X-APP-Key": env("APP_KEY"),
                "content-type": "application/json"
            }
    return headers

def grantTokenData():
    url = env("BASE_URL") + "/tokenized/checkout/token/grant"
    payload = {
                "app_key": env("APP_KEY"),
                "app_secret": env("APP_SECRET")
            }
    headers = {
                "accept": "application/json",
                "username": env("BKASH_USERNAME"),
                "password": env("BKASH_PASSWORD"),
                "content-type": "application/json"
            }
    return(url,payload,headers)

def createPaymentData(id_token):
    url = env("BASE_URL") + "/tokenized/checkout/create"
    payload = {
                "mode": "0011",
                "payerReference": "99",
                "callbackURL": "http://127.0.0.1:8000/execute",
                "merchantAssociationInfo": "MI05MID54RF09123456One",
                "amount": "50",
                "currency": "BDT",
                "intent": "sale",
                "merchantInvoiceNumber": "Inv0124"
            }
    headers = getHeaders(id_token)
    return(url,payload,headers)

def executeData(paymentID, id_token):
    url = env("BASE_URL") + "/tokenized/checkout/execute"
    payload = {
                "paymentID": paymentID
            }
    headers = getHeaders(id_token)
    return(url, payload, headers)

def createAgreementData(id_token):
    url = env("BASE_URL") + "/tokenized/checkout/create"
    
    payload = {
            "mode": "0000",
            "payerReference": "99",
            "callbackURL": "http://localhost:8000/execute"
        }
    headers = getHeaders(id_token)
    return(url, payload, headers)

def cancelAgreementData(id_token, agreementID):
    url = env("BASE_URL") + "/tokenized/checkout/agreement/cancel"
    
    payload = {
                "agreementID": agreementID,
        }
    headers = getHeaders(id_token)
    return(url, payload, headers)

def createPaymentWithAgreementData(id_token, agreementID):
    url = env("BASE_URL") + "/tokenized/checkout/create"
    payload = {
                "agreementID": agreementID,
                "mode": "0001",
                "payerReference": "99",
                "callbackURL": "http://127.0.0.1:8000/execute",
                "merchantAssociationInfo": "MI05MID54RF09123456One",
                "amount": "50",
                "currency": "BDT",
                "intent": "sale",
                "merchantInvoiceNumber": "Inv0124"
            }
    headers = getHeaders(id_token)
    return(url,payload,headers)

def refundData(id_token, paymentID, trxID):
    url =  env("BASE_URL") + "/tokenized/checkout/payment/refund"
    payload = {
        "amount": "50",
        "paymentID": paymentID,
        "trxID": trxID,
        "sku": "test",
        "reason": "yes"
    }
    headers = getHeaders(id_token)
    return(url, payload, headers)

def statusData(status, paymentID, trxID):
    data = {
        "statusMessage" : status,
        "paymentID" : paymentID,
        "trxID" : trxID
    }
    return(data)

def agreementStatusData(status, paymentID, agreementID):
    data = {
        "statusMessage" : status,
        "paymentID" : paymentID,
        "agreementID" : agreementID
    }
    return(data)

def indexData(agreementData):
    if len(agreementData)==0:
        return ({"customerMsisdn" : ""})
    return({"customerMsisdn" : agreementData[0].customerMsisdn})

