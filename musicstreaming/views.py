from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from .urls import url
from django.shortcuts import render
# from .forms import UploadFileForm
from .models import User, Music, Track, Forkship, UploadFile
import os


# Create your views here.
def index(request):
    return render(request, 'musicstreaming/index.html', {'worked': True})


def user_feed(request):
    return render(request, 'musicstreaming/user_feed.html', {})


def dashboard(request):
    if request.method == 'GET':
        path_list = request.path.split('/')
        user = path_list[2]
        # user_id = User.objects.filter(user_name=user)[0].user_id
        project = path_list[3]
        music_id = Music.objects.filter(music_name=project)[0].music_id
        # fs = Forkship.objects.filter(user=user_id, music=music_id)
        tracks = Track.objects.filter(music_id=music_id)
        track_list = []
        for track in tracks:
            print track.track_id
            track_list.append(track.track_id)
        response = {'tracks': track_list}
        server_info = " ec2-user@ec2-52-23-200-94.compute-1.amazonaws.com:"
        for track in track_list:
            path = '~/'
            # path += user
            # path += '/'
            # path += project
            # path += '/'
            path += Track.objects.filter(track_id=track)[0].track_name
            t = Track.objects.get(track_id=track)
            t.pathname = path
            t.save()
            # obj = open(Track.objects.filter(track_id=track)[0].track_name, 'w+')
            cmd = "scp -i ~/Downloads/bdeloeste.pem /tmp/" + \
                  Track.objects.filter(track_id=track)[0].track_name + \
                  server_info + path
            os.system(cmd)
        return render(request, 'musicstreaming/project_dashboard.html',
                      response)


        # print request.path.split('/')
    if request.method == 'POST':
        name = request.POST.get('username')
        uid = User.objects.filter(user_name=name)
        music_list = Forkship.objects.filter(user=uid).values()
        resp_list = []
        for music in music_list:
            m = Music.objects.filter(music_id=music['music_id'])
            print m[0].music_name
            resp_list.append(m[0].music_name)
        response = {'music_list': {'name': name, 'list': resp_list}}
        print response
        return render(request, 'musicstreaming/dashboard.html', response)
    raise Http404("Kurt's a fuck up, sorry")


def upload(request):
    if request.method == 'POST':
        print request.FILES
        # form = UploadFileForm(request.POST, request.FILES)
        # new_file = UploadFile(file = request.FILES['file'])
        # new_file.save()

        return HttpResponseRedirect('dashboard')