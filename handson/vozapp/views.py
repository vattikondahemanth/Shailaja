from django.shortcuts import render
from . models import Employee
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse

# Create your views here.


def content_list(request):
    content_data=Employee.objects.all()[:1000]
    return render(request, 'vozapp/content_list1.html', {'content_data': serializers.serialize('json', content_data)})

def content_list1(request):

    pageNo=request.GET.get('page')
    def chunked_iterator(queryset,chunk_size=1000):
        paginator=Paginator(queryset,chunk_size)
        total_pages=paginator.num_pages
        print('hhh',total_pages)
        if pageNo:
            contents=paginator.page(pageNo)
        else:
            contents=paginator.page(1)
        yield contents,total_pages
    for content_data,total_pages in chunked_iterator(Employee.objects.all()):
        if pageNo:
            data=serializers.serialize('json',content_data)
            return HttpResponse(data,content_type='application/json')
        else:
            return render(request,'vozapp/content_list2.html',{'content_data':serializers.serialize('json',content_data),'count':total_pages,'pno':pageNo})

