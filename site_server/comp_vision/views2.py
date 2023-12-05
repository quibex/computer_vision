from django.shortcuts import render, get_object_or_404, redirect
from django.http import StreamingHttpResponse, HttpResponse
from comp_vision.forms import BagFile
from comp_vision.models import Videos
from pathlib import Path
import os
from comp_vision.yolo.yolo1 import SaveVideoFile
from comp_vision.service import open_file



def index(request):
    if request.method == 'POST':
        form = BagFile( data=request.POST, files=request.FILES)
        if form.is_valid() and (request.FILES.__len__() != 0):
            video = form.save(commit=False)
            if request.user.id == None:
                video.user_id = 2
            else:
                video.user_id = request.user.id
            try:
                last_file = Videos.objects.filter(user_id=video.user_id).latest('id')
            except Videos.DoesNotExist:
                last_file = None


            video.save()
            parc_video_id = Videos.objects.last().id

            #delete last user's videos
            if last_file != None:
                try :
                    os.remove(str("files/" + str(last_file.bag_file)))
                    os.remove(str("files/" + str(last_file.parsed_video)))
                except:
                    pass

            return redirect('comp_vision:processing', parc_video_id)
        else:
            print(form.errors)
    else:
        form = BagFile()

    context = {
        'title': '1.1.1.1',
        'form': form,
        'status': False
    }
    return render(request, 'comp_vision/index.html', context)

def processing(request, pk: int):
    vidoe_mp4 = get_object_or_404(Videos, id=pk)

    vidoe_mp4.parsed_video = SaveVideoFile(vidoe_mp4.bag_file, vidoe_mp4.user_id)
    if str(vidoe_mp4.bag_file).split(".")[-1] != "mp4":
        vidoe_mp4.rgb_video = vidoe_mp4.bag_file
        vidoe_mp4.depth_video = vidoe_mp4.bag_file
    vidoe_mp4.cnt_man = 96
    vidoe_mp4.save()
    status = True
    context = {
        'title': '1.1.1.1',
        'video': vidoe_mp4,
        'status': status
    }
    if status:
        return redirect('comp_vision:result', pk)
    else:
        return render(request, 'comp_vision/index.html', context)

def result(request, pk: int):
    video_notexist = False
    video_is_mp4 = False
    try:
        video = get_object_or_404(Videos, id=pk)
        size1 = round(os.path.getsize(video.parsed_video.path)/1024/1024, 2)
        if str(video.bag_file).split(".")[-1] != "mp4":
            size2 = round(os.path.getsize(video.rgb_video.path)/1024/1024, 2)
            size3 = round(os.path.getsize(video.depth_video.path)/1024/1024, 2)
        else:
            size2, size3 = 0, 0
            video_is_mp4 = True
    except Videos.DoesNotExist:
        video_notexist = True
    context = {
        'video': video,
        'size1': size1,
        'size2': size2,
        'size3': size3,
        'video_notexist': video_notexist,
        'video_is_mp4': video_is_mp4,
    }
    return render(request, 'comp_vision/result.html', context)

def download_parc_file(request, pk: int):
    vidoe_mp4 = get_object_or_404(Videos, id=pk)
    file_path = "files/" + str(vidoe_mp4.parsed_video)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response

def download_rgb_file(request, pk: int):
    vidoe_mp4 = get_object_or_404(Videos, id=pk)
    file_path = "files/" + str(vidoe_mp4.rgb_video)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response
        
def download_depth_file(request, pk: int):
    vidoe_mp4 = get_object_or_404(Videos, id=pk)
    file_path = "files/" + str(vidoe_mp4.depth_video)
    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
        return response


def streemming_parc_video(request, pk: int):
    _video = get_object_or_404(Videos, id=pk)
    path = Path(_video.parsed_video.path)
    file, status_code, content_length, content_range = open_file(request, path)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

def streemming_rgb_video(request, pk: int):
    _video = get_object_or_404(Videos, id=pk)
    path = Path(_video.rgb_video.path)
    file, status_code, content_length, content_range = open_file(request, path)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

def streemming_depth_video(request, pk: int):
    _video = get_object_or_404(Videos, id=pk)
    path = Path(_video.depth_video.path)
    file, status_code, content_length, content_range = open_file(request, path)
    response = StreamingHttpResponse(file, status=status_code, content_type='video/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_length)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = content_range
    return response

