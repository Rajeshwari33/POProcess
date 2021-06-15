import requests
import logging
import json

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
        response = requests.get(post_url, data=payload)
        logging.info(response)
        if response == "Success":
            return True
        else:
            return False

    except Exception as e:
        logging.error(str(e))
        logging.error("Error in Getting Response from mail send", exc_info=True)
        return False