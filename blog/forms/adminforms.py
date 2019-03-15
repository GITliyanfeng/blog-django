# -*- coding: utf-8 -*-
# @Time    : 2019/3/13 0013 19:07
# @Author  : __Yanfeng
# @Site    : 
# @File    : adminforms.py
# @Software: PyCharm
from dal import autocomplete
from django import forms
from blog.models import Category, Tag, Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

"""自定义django admin的form"""


class PostAdminForm(forms.ModelForm):
    # desc 字段以大文本框的形式显式
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='categoryAutocompete'),
        label='分类',
    )
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tagAutocomplele'),
        label='标签',
    )
    content_ck = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=False)
    content_md = forms.CharField(widget=forms.Textarea(), label='正文', required=False)
    content = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Post
        fields = ('category', 'tag', 'title', 'desc', 'is_markdown', 'content', 'content_ck', 'content_md', 'status')

    def __init__(self, instance=None, initial=None, **kwargs):
        initial = initial or {}
        if instance:
            if instance.is_markdown:
                initial['content_md'] = instance.content
            else:
                initial['content_ck'] = instance.content
        super(PostAdminForm, self).__init__(instance=None, initial=None, **kwargs)

    def clean(self):
        is_markdown = self.cleaned_data.get('is_markdown')
        if is_markdown:
            content_field_name = 'content_md'
        else:
            content_field_name = 'content_ck'
        content = self.cleaned_data.get(content_field_name)
        if not content:
            self.add_error(content_field_name, '必须选择')
            return
        self.cleaned_data['content'] = content
        return super(PostAdminForm, self).clean()

    class Media:
        js = ('js/post_editor.js',)
