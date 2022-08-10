from django.shortcuts import render
from . models import Employee
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Q

# Create your views here.


def content_list(request):
    content_data=Employee.objects.all()[:1000]
    content_data1 = list(content_data)
    content_data1.insert(0, Employee(0 , "", 0))
    return render(request, 'vozapp/content_list1.html', {'content_data': serializers.serialize('json', content_data1)})

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



def column_search(request):
    import pdb
    # pdb.set_trace()
    print("search method is called")
    search_text=request.GET.get('searchString')
    search_values = search_text.split('|')
    emp_val = ""
    salary_val = 0
    emp_val =  search_values[0]
    salary_val = search_values[1] if len(search_values) > 1 else 0
    print(emp_val)
    print(salary_val)
    salary_val = int(salary_val)
    if emp_val and salary_val:
        print("both values")
        content_data = Employee.objects.filter(Q(name__contains=emp_val) & Q(salary__contains=salary_val))[:10]
        for i in content_data:
            print(i.name,i.salary)
    elif emp_val:
        print("emp values")
        content_data = Employee.objects.filter(Q(name__contains=emp_val))[:1000]
    elif salary_val:
        print("salary values")
        content_data = Employee.objects.filter(Q(salary__contains=salary_val))[:1000]

    content_data1 = list(content_data)
    print("querying completed")
    print(len(content_data))
    content_data1.insert(0, Employee(0, emp_val, salary_val))
    return HttpResponse(serializers.serialize('json', content_data1),content_type='application/json')
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Headers"] = "*"
    # return response