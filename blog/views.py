from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator


# Create your views here.
class IndexView():
    '''
    首页
    '''
    # 友情链接类型
    