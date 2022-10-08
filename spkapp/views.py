from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import order_form
from .models import order_model, Category, Product
from django.http import HttpResponseRedirect, HttpResponse
import csv


# Create your views here.

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
    # if this is a POST request we need to process the form data
    #  if request.method == 'POST':
    # create a form instance and populate it with data from the request:
    # form = NameForm(request.POST)
    # check whether it's valid:
    # if form.is_valid():
    # process the data in form.cleaned_data as required
    # ...
    # redirect to a new URL:
    # return HttpResponseRedirect('/thanks/')
    #     return redirect('dohome')
    # if a GET (or any other method) we'll create a blank form
    # else:
    # form = NameForm()

    return render(request, 'order/new_order.html', {})


def viewOrder(request):
    all_orders = order_model.objects.all()
    return render(request, 'order/view_order.html', {'all': all_orders})


def editOrder(request, order_id):
    order = order_model.objects.get(pk=order_id)
    form = order_form(request.POST or None, instance=order)
    if form.is_valid():
        task_list = form.save(commit=False)
        task_list.approver = request.user.username
        task_list.save()
        return redirect('approveorder')
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
    category_id = request.GET.get('category_id')
    print(category_id)
    products = Product.objects.filter(category_id=category_id).all()
    return render(request, 'persons/city_dropdown_list_options.html', {'cities': products})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


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
        ['#', 'Order Date', 'Requester', 'Project Name', 'Product Category', 'Product', 'Quantity', 'Remarks',
         'Approver', 'Approved Date', 'Status'])

    # loop through the order
    i = 0
    for order in orders:
        i = i + 1
        writer.writerow(
            [i, order.order_date, order.requester, order.projectname, order.category, order.product, order.quantity,
             order.remarks, order.approver, order.approved_date, order.status])

    return response
