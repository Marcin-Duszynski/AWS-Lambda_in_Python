import os
import json
import requests
import boto3
import base64

smmtApiUrl = None
snntApiKey = None

def handler(event, context):
    config = getRecallsConfiguration() 
    recall = sendRecallApiRequest("AISXXXTEST1239607", "BRUIN", config)

    return recall

def getRecallsConfiguration():
    global smmtApiUrl
    global snntApiKey

    if smmtApiUrl is None:
        smmtApiUrl = os.environ['SMMT_API_URI']
        print("Refreshing SNNT api url from OS")

    if snntApiKey is None:
        session = boto3.session.Session()
        kms = session.client('kms')

        encryptedSmmtApiKey = base64.b64decode(os.environ['SMMT_API_KEY'])
        snntApiKey = kms.decrypt(CiphertextBlob = encryptedSmmtApiKey)['Plaintext'].decode("ascii")
        print("Refreshing SNNT api key from OS")

    return {
        "snntApiUri": smmtApiUrl,
        "snntApiKey": snntApiKey
    }

def sendRecallApiRequest(vin, marque, config):
    header = {'Content-Type': 'application/json'}
    body = {
        "apikey": config["snntApiKey"],
        "Marque": marque,
        "VIN": vin
    }

    response = requests.post(config["snntApiUri"] + "/vincheck", headers = header, data = json.dumps(body))
    print(response.status_code)

    return {
        "statusCode": 200,
        "body": json.dumps(response.json())
    }
