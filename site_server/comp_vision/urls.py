from django.urls import path

from comp_vision.views import index, result, processing, streemming_parc_video, streemming_rgb_video, streemming_depth_video, download_parc_file, download_depth_file, download_rgb_file

app_name = 'comp_vision'

urlpatterns = [
    path('', index, name='index'),
    path('result/<int:pk>', result, name='result'),
    path('processing/<int:pk>', processing, name='processing'),
    path('stream_parc/<int:pk>', streemming_parc_video, name='streem_parc'),
    path('stream_rgb/<int:pk>', streemming_rgb_video, name='streem_rgb'),
    path('stream_depth/<int:pk>', streemming_depth_video, name='streem_depth'),
    path('download_parc/<int:pk>', download_parc_file, name='download_parc_file'),
    path('download_rgb/<int:pk>', download_rgb_file, name='download_rgb_file'),
    path('download_depth/<int:pk>', download_depth_file, name='download_depth_file'),
]
