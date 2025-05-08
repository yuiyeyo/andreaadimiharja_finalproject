from django import forms
from .models import Article, Advertisement
from django.contrib.auth.models import User
from .models import Profile
from .models import Article, Tag

class ProfileForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Profile
        fields = ['interests', 'subscriptions', 'disliked_topics']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class SearchForm(forms.Form):
    query = forms.CharField(required=False)
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    min_rating = forms.IntegerField(required=False, min_value=0)




class ArticleForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Article
        fields = ['headline', 'content', 'image_filename', 'video_filename', 'tags']

class AdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = ['headline', 'file_url', 'file_type', 'article']