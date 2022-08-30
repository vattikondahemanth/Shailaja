from django.contrib.postgres.search import SearchVector, SearchQuery
from django.shortcuts import render
from . models import Employee
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
import json

# Create your views here.

column_ddl_mapper = {
    "0" : "name",
    "1": "salary"

}

def content_list(request):
    content_data=Employee.objects.all().order_by('name')[:5000]
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
        content_data = Employee.objects.filter(Q(name__contains=emp_val) & Q(salary__contains=salary_val)).order_by('name')[:100]
        for i in content_data:
            print(i.name,i.salary)
    elif emp_val:
        print("emp values")
        content_data = Employee.objects.filter(Q(name__contains=emp_val)).order_by('name')[:5000]
    elif salary_val:
        print("salary values")
        content_data = Employee.objects.filter(Q(salary__contains=salary_val)).order_by('name')[:5000]
    elif emp_val == "":
        print("empty emp_val")
        content_data = Employee.objects.all().order_by('name')[:5000]


    content_data1 = list(content_data)
    print("querying completed")
    print(len(content_data))
    content_data1.insert(0, Employee(0, emp_val, salary_val))
    return HttpResponse(serializers.serialize('json', content_data1),content_type='application/json')
    # response["Access-Control-Allow-Origin"] = "*"
    # response["Access-Control-Allow-Headers"] = "*"
    # return response



def ajax_infinite(request):
    rowcount = int(request.GET.get('rowcount'))
    rowcount=rowcount+100
    emp=Employee.objects.all()[:rowcount]
    return HttpResponse(serializers.serialize('json', emp), content_type='application/json')

def get_all_drop_downs_data(request):
    search_value = request.GET.get("search")
    ddlcount = int(request.GET.get("ddlcount"))
    result = []
    contents = {}
    for i in column_ddl_mapper.keys():
        contents = get_distinct_col_values(i, search_value, ddlcount, page_offset=100)
        result.append(contents)
    return JsonResponse(result,safe=False)


def get_distinct_col_values(drop_down_number, search_value, current_row_num, page_offset=100):
    contents = {}
    filter_count = current_row_num + page_offset
    if drop_down_number:
        column_name = column_ddl_mapper[drop_down_number]
        dynamic_filter = {column_name + "__icontains": search_value}
        column_data = Employee.objects.order_by(column_name).values_list(column_name, flat=True).filter(
            **dynamic_filter).distinct(column_name)[:filter_count]
        column_data1 = Employee.objects.order_by(column_name).values_list(column_name, flat=True).filter(
            **dynamic_filter).distinct(column_name)
        contents = {
            drop_down_number: list(column_data)
        }

    if '0' in contents:
        print(len(contents['0']))
    print('column_data1',len(column_data1))
    return contents


def get_single_drop_downs_data(request):
    drop_down_number = request.GET.get("ddl_num")
    search_value = request.GET.get("ddl_val")
    current_row_num = int(request.GET.get("current_row_num"))

    contents = get_distinct_col_values(drop_down_number, search_value, current_row_num, page_offset=1000)

    return JsonResponse(contents)


def get_hands_on_table_data(request):
    hot_filter_values = request.GET.get("hot_filter_values")
    print('hot_filter_values',hot_filter_values)
    hot_filter_values = json.loads(hot_filter_values)

    # hot_filters = {"0": ["Employee 199123", "Employee 299123", "Employee 399123", "Employee 499123", "Employee 599123", "Employee 699123", "Employee 799123", "Employee 899123", "Employee 99123", "Employee 991230", "Employee 991231", "Employee 991232", "Employee 991233", "Employee 991234", "Employee 991235", "Employee 991236", "Employee 991237", "Employee 991238", "Employee 991239", "Employee 999123"], "1": [99123]}
    final_criterion = Q()
    for i in hot_filter_values.keys():
        col_filters = hot_filter_values[i]
        criterion = Q()
        if col_filters:
            for j in col_filters:
                search_val = j.split(":")[1].strip()
                column_name = j.split(":")[0].strip()
                dynamic_filter = {column_name + "__icontains": search_val}
                criterion |= Q(**dynamic_filter)
            final_criterion |= criterion

    data = Employee.objects.order_by('name').filter(final_criterion)[:2000]
    contents = serializers.serialize('json', data)
    return HttpResponse(contents, content_type='application/json')

def elid(request):
    return render(request,"vozapp/elided_pagination.html")

def home(request):
    content_data=Employee.objects.all().order_by('name')[:5000]
    content_data1 = list(content_data)
    content_data1.insert(0, Employee(0 , "", 0))
    return render(request, 'vozapp/single_dd.html', {'content_data': serializers.serialize('json', content_data1)})







