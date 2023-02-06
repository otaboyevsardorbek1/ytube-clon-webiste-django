from django.shortcuts import render, redirect
from .models import User, File_Upload
from django.contrib import messages

# Create your views here.
def index(request):
    if 'user' in request.session:
        all_files = File_Upload.objects.all()
        data = {'files': all_files}
        return render(request, 'index.html', data)
    else:
        return redirect('login')

def login(request):
    if 'user' not in request.session:
        if request.method == 'POST':
            email = request.POST['email']
            pwd = request.POST['pwd']
            userExists = User.objects.filter(email=email, pwd=pwd)
            if userExists.exists():
                request.session["user"] = email
                return redirect('index')
            else:
                messages.warning(request, "Wrong user or details.")
        return render(request, 'login.html')
    else:
        return redirect('index')


def logout(request):
    del request.session['user']
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        pwd = request.POST['pwd']
        gender = request.POST['gender']
        if not User.objects.filter(email=email).exists():
            create_user = User.objects.create(name=name, email=email, pwd=pwd, gender=gender)
            create_user.save()
            messages.success(request, "Your account is created successfully!")
            return redirect('login')
        else:
            messages.warning(request, "Email is already registered!")
        
    return render(request, 'signup.html')


def settings(request):
    if 'user' in request.session:
        user_obj = User.objects.get(email = request.session['user'])
        user_files = File_Upload.objects.filter(user = user_obj)

        img_list = []
        audio_list = []
        videos_list = []
        pdfs_list = []

        for file in user_files:
            if str(file.file_field)[-3:] == 'mp3':
                audio_list.append(file)
            elif str(file.file_field)[-3:] == 'mp4' or str(file.file_field)[-3:] == 'mkv':
                videos_list.append(file)
            elif str(file.file_field)[-3:] == 'jpg' or str(file.file_field)[-3:] == 'png' or str(file.file_field)[-3:] == 'jpeg':
                img_list.append(file)
            elif str(file.file_field)[-3:] == 'pdf':
                pdfs_list.append(file)  

        data = {'user_files': user_files, 'videos': len(videos_list), 'audios': len(audio_list), 'images': len(img_list), 'pdf': len(pdfs_list), 'img_list': img_list, 'audio_list': audio_list, 'videos_list': videos_list, 'pdfs_list': pdfs_list}
        return render(request, 'settings.html', data)

def file_upload(request):
    if request.method == 'POST':
        title_name = request.POST['title']
        description_name = request.POST['description']
        file_name = request.FILES['file_to_upload']

        user_obj = User.objects.get(email=request.session['user'])
        new_file = File_Upload.objects.create(user = user_obj, title=title_name, description=description_name, file_field = file_name)
        messages.success(request, "File is uploaded successfully!")
        new_file.save()
    return render(request, 'file_upload.html')

def delete_file(request, id):
    if 'user' in request.session:
        file_obj = File_Upload.objects.get(id = id)
        file_obj.delete()
        return redirect('settings')
    else:
        return redirect('login')