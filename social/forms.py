import logging

from bootstrap_modal_forms.forms import BSModalForm
from django import forms

from .models import Comment, Post

logger = logging.getLogger(__name__)


class PostCreateForm(forms.ModelForm):
    # If using CrispyForms, the only way to change background of textarea
    # is to define style here. With CSS selector it's not working.
    content = forms.CharField(
        label='',
        max_length=280,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                # 'cols': 30,
                'style': 'resize:none;',
                #   'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
                'placeholder': 'What\'s up?',
            }),
    )
    location = forms.CharField(
        label='Where are you at?',
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={
            'placeholder': 'Helsinki, Finland',
        }),
    )
    # To remove 'Currently photo' and 'Clear' field,
    # use this after required: widget=forms.FileInput
    image = forms.ImageField(
        label='Got any photo?',
        required=False,
        widget=forms.FileInput,
    )

    class Meta:
        model = Post
        fields = ['content', 'location', 'image']


class PostCreateFormModal(PostCreateForm, BSModalForm):
    pass


class PostUpdateForm(forms.ModelForm):
    # If using CrispyForms, the only way to change background of textarea
    # is to define style here. With CSS selector it's not working.
    content = forms.CharField(
        required=False,
        label='Edit content:',
        max_length=280,
        widget=forms.Textarea(
            attrs={
                'rows': 4,
                # 'cols': 30,
                'style': 'resize:none;',
                #   'style': 'resize:none; background-color: #15181c; color: #d9d9d9;',
                'placeholder': 'Text of your post',
            }),
    )
    location = forms.CharField(
        label='Edit location:',
        required=False,
        max_length=40,
        widget=forms.TextInput(attrs={
            'placeholder': 'Helsinki, Finland',
        }),
    )
    # To remove 'Currently photo' and 'Clear' field,
    # use this after required: widget=forms.FileInput
    image = forms.ImageField(
        label='Change current image for new one:',
        required=False,
        widget=forms.FileInput,
    )
    delete_current_image = forms.BooleanField(
        label='or only delete current (checkbox):',
        required=False,
    )

    class Meta:
        model = Post
        fields = ['content', 'location', 'image']


class PostUpdateFormModal(PostUpdateForm, BSModalForm):
    pass


class CommentCreateForm(forms.ModelForm):
    text = forms.CharField(
        max_length=280,
        label='',
        widget=forms.Textarea(
            attrs={
                'rows': 3,
                'cols': 10,
                # 'style': 'resize:none;',
                'style':
                'resize:none; background-color: #000000; color: #d9d9d9;',
                'placeholder': 'Leave your comment',
            }),
    )

    class Meta:
        model = Comment
        fields = ['text']


class CommentCreateFormModal(CommentCreateForm, BSModalForm):
    pass
