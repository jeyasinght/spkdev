from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import order_form
from .models import order_model, Product, Projects, Category, Units, Vendor
from django.http import HttpResponseRedirect, HttpResponse
import csv
import datetime
from django.db.models import Sum

# Create your views here.

def dologin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dohome')
            # Redirect to a success page.
        else:
            messages.success(request, "There was an error, Try login again...!")
            return redirect('dologin')
            # Return an 'invalid login' error message
    else:
        return render(request, 'login/dologin.html')


def dohome(request):
    all_orders = order_model.objects.all()
    return render(request, 'home/dohome.html', {'all': all_orders})


def dologout(request):
    logout(request)
    messages.success(request, "You were logged out ...!")
    return redirect('dologin')


def newOrder(request):
    return render(request, 'order/new_order.html', {})


def viewOrder(request):
    all_orders = order_model.objects.all()
    return render(request, 'order/view_order.html', {'all': all_orders})


def editOrder_old(request, order_id):
    order = order_model.objects.get(pk=order_id)
    form = order_form(request.POST or None, instance=order)
    if form.is_valid():
        task_list = form.save(commit=False)
        task_list.approver = request.user.username
        task_list.save()
        return redirect('approveorder')
    return render(request, 'order/edit_order.html', {'order': order, 'form': form})

def editOrder(request, order_id):
    order = order_model.objects.get(pk=order_id)
    form = order_form(request.POST or None, instance=order)
    if request.method == 'POST':
        oprojectname = request.POST.get('projectname')
        projectname = Projects.objects.get(id=oprojectname)
        ocategory = request.POST.get('category')
        category = Category.objects.get(id=ocategory)  
        oproduct = request.POST.get('product')
        product = Product.objects.get(id=oproduct)
        quantity = request.POST.get('quantity')
        ounit = request.POST.get('unit')
        unit = Units.objects.get(id=ounit)
        ovendor = request.POST.get('vendor')
        if ovendor != "":
            vendor = Vendor.objects.get(id=ovendor)
            order.vendor = vendor
        remarks = request.POST.get('remarks')
        status = request.POST['status']
        order.category = category
        order.projectname = projectname
        order.product = product
        order.quantity = quantity
        order.remarks = remarks
        order.status = status
        order.unit = unit
        order.approver = request.user.username
        order.save()
        submitted =True
        return render(request, 'order/postorderform.html', {'submitted': submitted})
    else:
         return render(request, 'order/edit_order.html', {'order': order, 'form': form})

def approveOrder(request):
    all_orders = order_model.objects.all()
    return render(request, 'order/approve_order.html', {'all': all_orders})


#def viewReport(request):
#    return render(request, 'report/viewreport.html', {})


def orderDetails(request):
    return render(request, 'order/order_detail.html', {})


def userRegistration(request):
    return render(request, 'registration/user_registration.html', {})


def formorder(request):
    submitted = False
    if request.method == "POST":
        form = order_form(request.POST)
        if form.is_valid():
            form.cleaned_data['order_date']
            task_list = form.save(commit=False)
            task_list.requester = request.user
            task_list.save()
            return HttpResponseRedirect('/formorder?submitted=True')
    else:
        form = order_form
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'order/postorderform.html', {'form': form, 'submitted': submitted})


def load_cities1(request):
    category_id = request.GET.get('category_id')
    products = Product.objects.filter(category_id=category_id).all()
    return render(request, 'persons/city_dropdown_list_options.html', {'cities': products})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def load_cities(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category=category).all()
    return render(request, 'order/orders.html', {'products': products})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def loadproducts(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'order/courses_dropdown_list_options.html', {'products': products})


def formorder1(request):
    submitted = False
    if request.method == "POST":
        form = order_form(request.POST)
        if form.is_valid():
            form.cleaned_data['order_date']
            task_list = form.save(commit=False)
            task_list.requester = request.user
            task_list.save()
            return HttpResponseRedirect('/formorder?submitted=True')
    else:
        form = order_form
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'order/test2.html', {'form': form, 'submitted': submitted})


def exporttoCSV(request):
    response = HttpResponse()
    response['content_type'] = 'text/csv'
    response['Content-Disposition'] = 'attachment;filename=order.csv'
    # create a CSV writer
    writer = csv.writer(response)
    orders = order_model.objects.all()
    # add column heading to CSV file

    writer.writerow(
        ['#', 'Order No','Order Date', 'Requester', 'Project Name', 'Product Category', 'Product', 'Quantity', 'Unit', 'Remarks',
         'Approver', 'Approved Date', 'Status'])

    # loop through the order
    i = 0
    for order in orders:
        i = i + 1
        writer.writerow(
            [i, order.orderno, order.order_date, order.requester, order.projectname, order.category, order.product, order.quantity,
             order.unit, order.remarks, order.approver, order.approved_date, order.status])

    return response

def orders(request):
    submitted = False
    if request.method == "POST":
        oprojectname = request.POST.get('projectname')
        projectname = Projects.objects.get(id=oprojectname)
        ocategory = request.POST.getlist('programming[]')
        oproduct = request.POST.getlist('product[]')
        oquantity = request.POST.getlist('quantity[]')
        ounit = request.POST.getlist('unit[]')
        oremarks = request.POST.getlist('remarks[]')
        order_date = datetime.datetime.now()
        status = "Requested"
        count = len(ocategory)
        orderno = order_model.objects.latest('id')
        orderno = orderno.pk
        for i in range(count):
            orderno = int(orderno) + 1
            category = Category.objects.get(id=ocategory[i])
            product = Product.objects.get(id=oproduct[i])
            quantity = oquantity[i]
            unit = Units.objects.get(id=ounit[i])
            remarks = oremarks[i]
            order = order_model()
            order.category = category
            order.order_date = order_date
            order.projectname = projectname
            order.product = product
            order.quantity = quantity
            order.remarks = remarks
            order.status = status
            order.unit = unit
            order.orderno = 'SPK-' + str(orderno).zfill(6) 
            order.requester = request.user
            order.save()
       # return HttpResponseRedirect('/orders?submitted=True')
        return render(request, 'order/postorderform.html', {'submitted': 'True'})
    else:
        projects = Projects.objects.all()
        categories = Category.objects.all()
        punits = Units.objects.all()
        return render(request, 'order/orders.html', {'cities': projects, 'categories': categories, 'punits': punits})


def viewReport(request):
    if request.method == "POST":
        odate = request.POST.get('order_date')
        #if odate == "":
       #     return render(request, 'report/report_dup.html', {'cities': projects, 'categories': categories, 'punits': punits,'mylist': mylist})
       # else:
        orders_new = order_model.objects.filter(order_date = odate).order_by("id")
        #  orders_new = order_model.objects.values('category','product').order_by().annotate(Sum('quantity'))
        # orders = order_model.objects.filter(projectname_id=oprojectname).order_by("id")
        # return HttpResponseRedirect('/orders?submitted=True')
        projects = Projects.objects.all()
        categories = Category.objects.all()
        stat= order_model._meta.get_field('status').choices
        mylist = [(stat[0][0]), (stat[1][0]), (stat[2][0])]
        return render(request, 'report/report.html', {'cities': projects, 'categories': categories,'orders': orders_new,'mylist': mylist})
    else:
        projects = Projects.objects.all()
        categories = Category.objects.all()
        punits = Units.objects.all()
        #stat= order_model.status
        stat= order_model._meta.get_field('status').choices
        mylist = [(stat[0][0]), (stat[1][0]), (stat[2][0]),(stat[3][0])]
        return render(request, 'report/report.html', {'cities': projects, 'categories': categories, 'punits': punits,'mylist': mylist})

def approveOrder_new(request, status):
    all_orders = order_model.objects.filter(status=status)
   # Model.objects.values('product', 'condition').order_by().annotate(Sum('quantity'))
    return render(request, 'order/approve_order.html', {'all': all_orders})

def viewReport_dup(request):
    if request.method == "POST":
        odate = request.POST.get('order_date')
     #   orders_new = order_model.objects.filter(order_date = odate).order_by("id").values
     #   item = order_model.objects.filter(order_date = odate).values()
        item = order_model.objects.filter(order_date = odate).values('projectname', 'category','product').annotate(Sum('quantity'))
        for course in item:
            projects = Projects.objects.filter(id=course['projectname']).values_list('name')
            for project in projects:
                project_name= project[0]
            course['projectname'] = project_name
            categories = Category.objects.filter(id=course['category']).values_list('name')
            for category in categories:
                category_name= category[0]
            course['category'] = category_name
            products = Product.objects.filter(id=course['product']).values_list('name')
            for product in products:
                product_name= product[0]
            course['product']= product_name
       # return HttpResponseRedirect('/orders?submitted=True')
        projects = Projects.objects.all()
        categories = Category.objects.all()
        stat = order_model._meta.get_field('status').choices
        mylist = [(stat[0][0]), (stat[1][0]), (stat[2][0])]
        return render(request, 'report/report_dup.html', {'cities': projects, 'categories': categories,'orders': item,'mylist': mylist})
    else:
        projects = Projects.objects.all()
        categories = Category.objects.all()
        punits = Units.objects.all()
        #stat= order_model.status
        stat= order_model._meta.get_field('status').choices
        mylist = [(stat[0][0]), (stat[1][0]), (stat[2][0]),(stat[3][0])]
        return render(request, 'report/report_dup.html', {'cities': projects, 'categories': categories, 'punits': punits,'mylist': mylist})