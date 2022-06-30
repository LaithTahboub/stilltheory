import json
import random
import string
import base64
import hashlib
from urllib.parse import urlencode
from aiohttp import web
from django.shortcuts import redirect
import requests

def auth():
    # login:
    code_verifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
    code_verifier = base64.urlsafe_b64encode(code_verifier.encode('utf-8'))

    code_challenge = hashlib.sha256(code_verifier).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
    #  is our tokenk lip_Al3w9AX8TW8puxBnPmE1
    # url = 'https://lichess.org/api/account'
    authorize_url = (
            'https://lichess.org/oauth'
            + "/?"
            + urlencode(
                {
                    "state": 'zwDR8BuZRckY0W0aVRgeZmZ7IV8FSO2u1zLIL5Yc5u72dTQOM5Nivlgiezk9fW0bxh8xKY47RmzRt9nsMLucObzS5TmHWO86EB6frBsm4qTlhRsO6dNSOTGwYeTKs2yU',
                    "client_id": '9Q1aqLsGmmRGJDWdUEgYocJwiZ7yfNO4YN8PR4er',
                    "response_type": "code",
                    "redirect_uri": 'http://127.0.0.1:8000/',
                    "code_challenge": code_challenge,
                    "code_challenge_method": "S256",
                }
            )
        )
    return redirect(authorize_url)

