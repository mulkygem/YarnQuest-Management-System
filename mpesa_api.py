import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import json
import re

class MpesaGateway:
    def __init__(self):
        self.consumer_key = "gXSb2lcdWO2MH8AZzHYCHsBzXhl6ceeyczZCpX4GGdxb8vX7"
        self.consumer_secret = "Mq1hkebfkeIhNf1Ej9TJTA3kYTSJGlotRvv4RE3V1Flnva2JbxJyb7TcDFWAjs9d"
    
        self.business_shortcode = "174379"
        self.passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        
        self.auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        self.stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    def get_access_token(self):
        try:
            response = requests.get(self.auth_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret))
            if response.status_code == 200:
                return response.json().get("access_token")
            return None
        except Exception as e:
            print(f"Error fetching access token: {e}")
            return None

    def trigger_stk_push(self, phone_number, amount, callback_url):
        
        access_token = self.get_access_token()
        if not access_token:
            return {"status": "error", "message": "Failed to authenticate with Safaricom gateway."}

        #Regex Phone Formatter
        phone_str = str(phone_number).strip().replace(" ", "").replace("+", "")
        match = re.search(r'(7\d{8}|1\d{8})$', phone_str)
        
        if match:
            phone_number = "254" + match.group(1)
        else:
            print(f"Error: Phone number formatting failed for layout input: {phone_number}")
            return {"status": "error", "message": "Invalid phone number format provided."}

        
        final_amount = int(float(amount))
        if final_amount < 1:
            final_amount = 1

        
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password_str = self.business_shortcode + self.passkey + timestamp
        password = base64.b64encode(password_str.encode()).decode('utf-8')

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": final_amount, 
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": "YarnQuestCrafts",
            "TransactionDesc": "Payment for Craft Supplies"
        }

        try:
            response = requests.post(self.stk_push_url, json=payload, headers=headers)
            print(f"--- Safaricom API Request Payload ---")
            print(json.dumps(payload, indent=2))
            print(f"--- Safaricom API Gateway Response ---")
            print(response.text)
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}
