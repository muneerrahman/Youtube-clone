from django.shortcuts import render
from django.views.generic.base import View,HttpResponse,HttpResponseRedirect
from .forms import LoginForm,RegisterForm,NewVideoForm,CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import string,random
from.models import Video, Comment
from pathlib import Path
from wsgiref.util import FileWrapper
from django.core.files.storage import FileSystemStorage
import os

class VideoFileView(View):
    def get(self, request, file_name):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file = FileWrapper(open(BASE_DIR+'/'+file_name, 'rb'))
        response = HttpResponse(file, content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        return response

class VideoView(View):
    template_name='video.html'
    def get(self, request, id):
        # fetch video from DB by ID
        video_by_id = Video.objects.get(id=id)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        video_by_id.path = 'http://localhost:8000/get_video/' + video_by_id.path
        context = {'video': video_by_id}

        if request.user.is_authenticated:
            Comment_form=CommentForm()
            context['form']=Comment_form
        comment=Comment.objects.filter(Video__id=id).order_by('-datetime')[:5]
        context['comments']=comment
        return render(request,self.template_name,context)

class HomeView(View):
    template_name='index.html'
    def get(self,request):
        most_recent_video=Video.objects.order_by('-datetime')[:10]
        return render(request,self.template_name,{'most_recent_video':most_recent_video})
class RegisterView(View):
    template_name='register.html'
    def get(self,request):
            if request.user.is_authenticated:
                print('aleady logged in')
                print(request.user)
                return HttpResponseRedirect('/')
            form=RegisterForm
            return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['username'])
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            email=form.cleaned_data['email']
            new_user=User(username=username,email=email)
            new_user.set_password(password)
            new_user.save()
            return HttpResponseRedirect('/login')
        return HttpResponse('this is a post request')
class LoginView(View):
    template_name='login.html'
    def get(self,request):
        if request.user.is_authenticated:
            print('aleady logged in')
            print(request.user)
            # logout(request)
            return HttpResponseRedirect('/')
        form=LoginForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form=LoginForm(request.POST)
        print(LoginForm(request.POST))
        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/login')
class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')

class NewVideo(View):
    template_name = 'new_video.html'
    def get(self, request):
        if request.user.is_authenticated==False:
            return HttpResponseRedirect('login')
        form=NewVideoForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = NewVideoForm(request.POST,request.FILES)
        print(request.FILES)
        if form.is_valid():
            title=form.cleaned_data['title']
            description=form.cleaned_data['description']
            file=form.cleaned_data['file']
            print(title)
            print(description)
            random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            path=random_string+file.name
            fs = FileSystemStorage(location=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            filename = fs.save(path, file)
            file_url = fs.url(filename)

            print(fs)
            print(filename)
            print(file_url)

            new_video = Video(title=title,description= description,user=request.user,path=path)
            new_video.save()
            print(new_video)
            return HttpResponseRedirect('/video/{}'.format(new_video.id))
        else:
            return HttpResponse('your form is not valid')

class CommentView(View):
    template_name='comment.html'
    def post(self,request):
        form=CommentForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['text']
            video_id=request.POST['video']
            video=Video.objects.get(id=video_id)
            new_comment=Comment(text=text,user=request.user, Video=video)
            new_comment.save()
            return HttpResponseRedirect('/video/{}'.format(str(video_id)))
        return HttpResponse('this is a post request')