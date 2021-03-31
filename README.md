# Version Requirements
<img src="https://img.shields.io/badge/Django-3.1.5-blue?style=for-the-badge">   <img src="https://img.shields.io/badge/PyJWT-2.0.1-red?style=for-the-badge">   <img src="https://img.shields.io/badge/DjangoRestFramework-3.12.2-green?style=for-the-badge"> 


# Description

Built token-based authentication library for authenticating users. Used HSA256 algorithm for token generation. Created proper API documentation using Swagger/ReDoc.


## Configure Settings

```python
# Configure JWT Settings
JWT_CONFIGURATION = {
    'TOKEN_LIFETIME': timedelta(days=7), #token expiry in 7days
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    
    'AUTH_HEADER':'Bearer',
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
}

# Specify User model for authentication
AUTH_USER_MODEL = 'userAuth.User'
```

## Usage
```python
class UserProfileAPI(RetrieveAPIView):
    permission_classes = [custom_permissions.IsTokenVerified]
    def get(self, request):
        pass
```
