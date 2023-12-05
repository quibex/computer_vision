from django.db import models
from django.core.validators import FileExtensionValidator

from users.models import User
class Videos(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    bag_file = models.FileField(upload_to='bag_files/',  validators=[FileExtensionValidator(allowed_extensions=['mp4', 'bag'])], null=True, blank=True)
    rgb_video = models.FileField(upload_to='rgb_video/', null=True, blank=True)
    depth_video = models.FileField(upload_to='depth_video/', null=True, blank=True)
    parsed_video = models.FileField(upload_to='parsed_video/', null=True, blank=True)
    cnt_man = models.PositiveIntegerField(default=0)
