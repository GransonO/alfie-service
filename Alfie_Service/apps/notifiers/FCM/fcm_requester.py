import json
import os

import requests
from dotenv import load_dotenv


class FcmRequester:

    @staticmethod
    def doctor_call_notice(all_tokens, message, user_id, session_id):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        load_dotenv()
        fcm_key = os.environ['ALFIE_FCM_KEY']

        my_headers = {
            "Authorization": "key={}".format(fcm_key),
            "content-type": "application/json"
        }

        message_body = {
            "title": "Therapy session",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png",
        }

        my_data = {
            "registration_ids": all_tokens,
            "notification": message_body,
            "data": {
                "patientId": user_id,
                "sessionID": session_id,
                "page": "TherapySession",
                "title": "Therapy session",
                "body": "Click to view the details",
            }
        }

        background = {
            "registration_ids": all_tokens,
            "data": {
                "patientId": user_id,
                "sessionID": session_id,
                "page": "TherapySession",
                "title": "Therapy session",
                "body": "Click to view the details",
            }
        }

        # y = requests.post(url, headers=myHeaders, data=json.dumps(background))
        x = requests.post(url, headers=my_headers, data=json.dumps(my_data))
        print("message sen ------------------------------------ : {}".format(x))

    @staticmethod
    def call_notice(all_tokens, message, doctor_id, session_id):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        load_dotenv()
        fcm_key = os.environ['ALFIE_FCM_KEY']

        my_headers = {
            "Authorization": "key={}".format(fcm_key),
            "content-type": "application/json"
        }

        message_body = {
            "title": "Therapy session",
            "text": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png",
        }

        my_data = {
            "registration_ids": all_tokens,
            # "notification": message_body,
            "data": {
                "doctorID": doctor_id,
                "sessionID": session_id,
                "page": "TherapySession",
                "title": "Therapy session update",
                "body": "Click to view the details",
            }
        }

        background = {
            "registration_ids": all_tokens,
            "data": {
                "doctorID": doctor_id,
                "sessionID": session_id,
                "page": "TherapySession",
                "title": "Therapy session",
                "body": "Click to view the details",
            }
        }

        # y = requests.post(url, headers=myHeaders, data=json.dumps(background))
        x = requests.post(url, headers=my_headers, data=json.dumps(my_data))
        print("message sen ------------------------------------ : {}".format(x))

    @staticmethod
    def subscribers_notice(all_tokens, message, media_type, media_id, uploader):
        """Send notification to the doctor"""
        url = 'https://fcm.googleapis.com/fcm/send'

        load_dotenv()
        fcm_key = os.environ['ALFIE_FCM_KEY']

        my_headers = {
            "Authorization": "key={}".format(fcm_key),
            "content-type": "application/json"
        }

        message_body = {
            "title": "New {} from {}".format(media_type, uploader),
            "body": message,
            "icon": "https://res.cloudinary.com/dolwj4vkq/image/upload/v1621418365/HelloAlfie/ic_launcher.png",
        }

        my_data = {
            "registration_ids": all_tokens,
            "notification": message_body,
            "data": {
                "media_id": str(media_id),
                "page": "open_media",
                "title": "Therapy session",
                "body": "Click to see the details",
            }
        }

        requests.post(url, headers=my_headers, data=json.dumps(my_data))

    @staticmethod
    def doctor_validation_notice(all_tokens, message):
        url = 'https://fcm.googleapis.com/fcm/send'

        load_dotenv()
        fcm_key = os.environ['ALFIE_FCM_KEY']

        my_headers = {
            "Authorization": "key={}".format(fcm_key),
            "content-type": "application/json"
        }

        my_data = {
            "registration_ids": all_tokens,
            "notification": {
                      "title": "Hello Alfie Doctor validation",
                      "body": message,
                      "icon": "request_icon"
                    }
        }

        # y = requests.post(url, headers=myHeaders, data=json.dumps(background))
        x = requests.post(url, headers=my_headers, data=json.dumps(my_data))
        print("message sen ------------------------------------ : {}".format(x))
