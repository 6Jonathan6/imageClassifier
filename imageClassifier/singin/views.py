import requests
from requests.auth import HTTPBasicAuth
from jose import jwt
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.conf import settings


#Keys de la user pool

def jwks():
    
    JWKS_URL = 'https://cognito-idp.{0}.amazonaws.com/{1}/.well-known/jwks.json'.format(settings.AWS_REGION,settings.POOL_ID)
    JWKS = requests.get(JWKS_URL).json()['keys']
    return JWKS


#Para revisar si el token viene de coginito

def verify(id_token,access_token,JWKS):
    
    header = jwt.get_unverified_header(id_token)
    
    key = [k for k in JWKS if k['kid'] == header['kid']][0]
    
    id_token = jwt.decode(id_token,key,audience=settings.APP_CLIENT_ID,access_token=access_token)
    
    return id_token
    

# Create your views here.

class HomeView(TemplateView):
    
    template_name = 'singin/HomeView.html'

def LoginView(request):
    
    url = '{0}/login?response_type=code&client_id={1}&redirect_uri={2}&scope=openid'.format(settings.APP_DOMAIN,settings.APP_CLIENT_ID,settings.CALLBACK_URL)
    return redirect(url)
        
    
def CallBackView(request):

#llaves de nuestra user pool
    JWKS = jwks()
    code = request.GET.__getitem__('code')
    
    
    #Intercambiamos el código por el token
    request_parameters = {
        
        'grant_type': 'authorization_code',
        'client_id': settings.APP_CLIENT_ID,
        'code':code,
        'redirect_uri':settings.CALLBACK_URL,
        
        
    }
        
    url = "{0}/oauth2/token".format(settings.APP_DOMAIN)
    response = requests.post(
        
        url,
        data = request_parameters,
        auth = HTTPBasicAuth(settings.APP_CLIENT_ID, settings.APP_CLIENT_SECRET))
        
        
    #desencriptamos el id_token   
    token = response.json()
    token_id = verify(token['id_token'],token['access_token'],JWKS)
        
    request.session.__setitem__('nickname',token_id['nickname'])
    request.session.__setitem__('logged',True)
        
    return redirect('home')
        
        
    