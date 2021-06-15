import requests
import logging
import json
from django.http import JsonResponse

def resend_approved_mail(to_email_id, body, subject, from_mail_id, password):
    try:
        post_url = "http://127.0.0.1:2022/sending/send_approved_email/"
        data = {
            "to_email_id" : to_email_id,
            "body" : body,
            "subject" : subject,
            "from_mail_id" : from_mail_id,
            "password" : password
        }
        payload = json.dumps(data)
        # print(payload)
        response = requests.get(post_url, data=payload)
        logging.info(response)
        # print(response)
        if response:
            return JsonResponse({"status" : "Success"})
        else:
            return JsonResponse({"status": "Error"})

    except Exception as e:
        print(str(e))
        logging.error(str(e))
        logging.error("Error in Getting Response from mail send", exc_info=True)
        return False