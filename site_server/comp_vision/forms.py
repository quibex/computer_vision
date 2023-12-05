from django import forms
from comp_vision.models import Videos


class BagFile(forms.ModelForm):
    bag_file = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'costum-file-input'}), required=False)


    class Meta:
        model = Videos
        fields = ("bag_file", )

class VideoForm(forms.Form):
    title = forms.CharField(max_length=50)
    video = forms.FileField()