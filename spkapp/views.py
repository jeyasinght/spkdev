import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import order_form
from .models import order_model, Product, Projects, Category, Units
from django.http import HttpResponseRedirect, HttpResponse
import csv
import datetime


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
    print(order)
    print(form)
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
        remarks = request.POST['remarks']
        order_date = datetime.datetime.now()
        status = request.POST['status']
        order.category = category
        order.order_date = order_date
        order.projectname = projectname
        order.product = product
        order.quantity = quantity
        order.remarks = remarks
        order.status = status
        order.unit = unit
        order.approver = request.user.username
        order.save()
        return redirect('approveorder')
    else:
        return render(request, 'order/edit_order.html', {'order': order, 'form': form})


def approveOrder(request):
    all_orders = order_model.objects.all()
    return render(request, 'order/approve_order.html', {'all': all_orders})


def viewReport(request):
    return render(request, 'report/viewreport.html', {})


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
    print(category_id)
    products = Product.objects.filter(category_id=category_id).all()
    return render(request, 'persons/city_dropdown_list_options.html', {'cities': products})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def load_cities(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category=category).all()
    print(products)
    return render(request, 'order/orders.html', {'products': products})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def loadproducts(request):
    category_id = request.GET.get('category')
    print(category_id)
    products = Product.objects.filter(category_id=category_id).order_by('name')
    print(products)
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
        ['#', 'Order Date', 'Requester', 'Project Name', 'Product Category', 'Product', 'Quantity', 'Unit', 'Remarks',
         'Approver', 'Approved Date', 'Status'])

    # loop through the order
    i = 0
    for order in orders:
        i = i + 1
        writer.writerow(
            [i, order.order_date, order.requester, order.projectname, order.category, order.product, order.quantity,
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
        for i in range(count):
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
            order.requester = request.user
            order.save()
        # return HttpResponseRedirect('/orders?submitted=True')
        return render(request, 'order/postorderform.html', {'submitted': 'True'})
    else:
        projects = Projects.objects.all()
        categories = Category.objects.all()
        punits = Units.objects.all()
        return render(request, 'order/orders.html', {'cities': projects, 'categories': categories, 'punits': punits})


def inventory(request):
    if request.method == "POST":
        oprojectname = request.POST.get('projectname')
        projectname = Projects.objects.get(id=oprojectname)

        orders = order_model.objects.filter(projectname_id=oprojectname).order_by("id")
        # ocategory = request.POST.get('programming')
        # oproduct = request.POST.get('product')
        # return HttpResponseRedirect('/orders?submitted=True')
        return render(request, 'report/report.html', {'orders': orders})
    else:
        projects = Projects.objects.all()
        categories = Category.objects.all()
        punits = Units.objects.all()
        return render(request, 'report/report.html', {'cities': projects, 'categories': categories, 'punits': punits})
