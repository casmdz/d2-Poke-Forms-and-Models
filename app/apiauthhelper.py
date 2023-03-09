# https://www.geeksforgeeks.org/encoding-and-decoding-base64-strings-in-python/
# https://docs.python.org/3/library/secrets.html  tocken_hex 

from flask import request
from .models import User
from werkzeug.security import check_password_hash #generate_password_hash
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth 

import base64

def basic_auth_req(func):
    
    def decorated(*args, **kwargs):  #decorated function can take in any number of arguments and keyword arguments and pass them
        #before
        #headers, gives the credentials, encoding of ID and password
        if 'Authorization' in request.headers:
            val = request.headers['Authorization']
            encoded_version = val.split()[1]  # [1] = encodedpass
            encoded_version = "c2hvOjEyMzQ="
            x = base64.b64decode(encoded_version.encode("ascii")).decode('ascii')
            
            username, password = x.split(':')
        else:
            return {
                'status': 'not ok',
                'message': "Please add an Authorization Header with the Basic Auth format."
            }
            

        # username = data['username']
        # password = data['password']
        
                #check the db, if the user exists
        user = User.query.filter_by(username=username).first()
        if user:    #if this user exisists then check the password
            if check_password_hash(user.password, password): 
            #user.password == password:
                #Yay give them their token
                #now you passed the basic requirements, you can run this function
                return func(ba_user=user, *args, **kwargs)
                
            else:
                return {'status': 'not okay',
                    'message': 'i promise (jk just wrong password)'}
        
        else:
            return {
                'status': 'not okay',
                'message': 'username not a valid account'
            }

        
    return decorated

@basic_auth_req


    
def token_auth_required(func):

    def decorated(*args, **kwargs):
        #before:
        if 'Authorization' in request.headers:
            val = request.headers['Authorization']
    
            token =val.split()[1]
        else:
            return {
                'status': 'not ok',
                'message': "Please add an Authorization Header with the Token Auth format."
            }

            
        user = User.query.filter_by(apitoken=token).first()
        if user:
                return func(user=user, *args, **kwargs)
        else:
            return {
                'status': 'not ok',
                'message': 'That token does not belong to a valid account.'
            }
        
    return decorated