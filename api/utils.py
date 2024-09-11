import datetime
import requests
import json

from api.models import OtpMail



def sms_sender(telephone, message, otp):
    try:
        base_url = "https://www.jawalbsms.ws/api.php/sendsms"
        params = {
            'user': 'FARES OTP',
            'pass': 'Fares31048116',
            'to': f'966{telephone}',
            'message': f'{message} {otp}',
            'sender': 'FARES OTP'
        }
        
    except Exception as e:
        return None
    try:
            
        response = requests.get(base_url, params=params, timeout=15)
        print(str(response.status_code)+" ==> "+str(response.text))
        if response.status_code==200:
            try:
                ot = OtpMail.objects.get(telephone=telephone)
                ot.otp=otp
                ot.created_at = datetime.datetime.now()
                ot.save()
            except:
                ot = OtpMail.objects.create(telephone=telephone,otp=otp)
    except Exception as e:
        return None
    else:
        if response.status_code in [200, 201]:
            return True
        else:
            return None
        
