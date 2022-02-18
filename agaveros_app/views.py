from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from agaveros_app.forms import FormRegistro
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import requests
from requests.structures import CaseInsensitiveDict

# Create your views here.

def index (request):
    formRegistrar = FormRegistro()
    return render(request,'index.html',{'form':formRegistrar})

def registro(request):
    if request.method=='POST':
        formRegistrar = FormRegistro(request.POST)
        isUsu = setUserApi(request)
        if formRegistrar.is_valid():
            if isUsu == 201:
                formRegistrar.save()
                messages.success(request,f"Te has registrado con exito")
                return redirect("index")
            else:
                messages.success(request,f"El correo ingresado ya ha sido registrado")
                return redirect("index")
        else:            
            messages.error(request,"Campos introduciondos invalidos")
            return redirect("index")

def iniciar_session (request):
    if request.method == 'POST':
        correo = request.POST.get('email')
        pwd = request.POST.get('pswd')
        params = {
            "correo" : correo,
            "clave" : pwd
        }
        if not correo:
            messages.error(request,"El campo correo esta vació")
            return redirect('index')
        if not pwd:
            messages.error(request,"El campo contraseña esta vació")
            return redirect('index')
        existeUsuario = isUser(params)
        if existeUsuario == 404:
            messages.success(request,"Correo o contraseña invalido")
            return redirect('index')
        if existeUsuario == 200:
            token =getUserToken(params)            
            user = authenticate(request,username=correo,password=pwd)
            if user is not None:
                login(request,user)
                resUsu = obtener_usuario(correo,token)
                request.session['token'] = token
                request.session['correo'] = resUsu['correo']
                #comprovacion de correo verificado
                if resUsu['confirmado'] == 0:
                    messages.success(request,f"Se envio un codigo de confirmación al correo : {request.session['correo']}")
                    return redirect('verificar')
                else:
                    messages.success(request,f"Bienvenido {request.session['correo']}")
                    return redirect('index_login')

@login_required(login_url='index')       
def exit_user(request):
    logout(request)
    return redirect('index')

@login_required(login_url='index')
def verificado(request):
    return render(request,'verificacion.html')

def confirmar(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        if not token:
            messages.error(request,"el campo esta vació")
            return render(request,'verificacion.html')
        #Peticion al api para actualizar la verificacion
        res = confirmEmail(request.session['token'],request.session['correo'],token)
        #comprovacion de codigo correcto
        if res == 404:
            messages.error(request,f"El código es incorrecto, vuelve a ingresar el codigo enviado a{request.session['correo']}")
            return redirect('verificar')
        if res == 200:
            messages.success(request,f"Bienvenido {request.session['correo']}")
            return redirect('index_login')

@login_required(login_url='index')
def index_login(request):
    return render(request,'login/index_login.html')

##########METODOS DEL API######
def setUserApi(request):
    user = request.POST.get('username')
    correo = request.POST.get('email')
    telefono = request.POST.get('first_name')
    pwd1 = request.POST.get('password1')
    url = "http://54.70.119.136:5000/auth/registrar"
    params = {
        "usuario" : user,
        "correo" : correo,
        "clave" : pwd1,
        "telefono" : telefono
    }          
    r = requests.post( url, json=params)
    return r.status_code  

def isUser(params):
    url = "http://54.70.119.136:5000/auth/login"
    r = requests.post( url, json=params)
    res = r.status_code
    return res

def getUserToken(params):    
    url = "http://54.70.119.136:5000/auth/login"
    r = requests.post( url, json=params)
    res = r.json()
    return res['access_token']

def confirmEmail(token,correo,codigo):
    url_usuario = 'http://54.70.119.136:5000/api/usuario/'+str(correo)
    params = {
        "token" : codigo
    }  
    headers = CaseInsensitiveDict()
    headers = {"Authorization": "Bearer "+str(token)}
    res = requests.put( url_usuario,headers=headers,json=params)
    return res.status_code

def obtener_usuario(correo,token):
    #se obtiene y alamcena el token
    tk = token
    url_usuario = 'http://54.70.119.136:5000/api/usuario/'+str(correo)
    headers = CaseInsensitiveDict()
    headers = {"Authorization": "Bearer "+str(tk)}
    res = requests.post( url_usuario,headers=headers)
    usu = res.json()
    return usu