import jwt
from re import sub
from datetime import datetime
from django.http import HttpResponseForbidden
from django.conf import settings




class CheckAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if header_token := request.META.get(f'{settings.JWT_CONFIGURATION["AUTH_HEADER_NAME"]}', None):
            try:
                token = sub(
                    pattern=f'{settings.JWT_CONFIGURATION["AUTH_HEADER"]} ',
                    repl='',
                    string=header_token
                )
                # decode the token here to get payload and header
                decoded_data = jwt.decode(token, settings.JWT_CONFIGURATION['SIGNING_KEY'], algorithms=settings.JWT_CONFIGURATION['ALGORITHM'])
                
                # checks if token is expired
                if datetime.strptime(decoded_data['token_expiry'], '%Y-%m-%d %H:%M:%S.%f') <= datetime.now():
                    msg = "Token has expired. Please login again."
                    return HttpResponseForbidden(msg)
                
                # sets the user attributes from token into request
                setattr(request, 'user_details', decoded_data)
                
            except Exception as e:
                return HttpResponseForbidden(str(e))
            
        response = self.get_response(request)

        return response