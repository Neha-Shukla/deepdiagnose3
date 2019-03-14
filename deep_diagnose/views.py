
from .filters import CompanyFilter
from django.views import generic
from .models import CompanyDetail, Tests,  CompanyTests, OrderInfo, TestCategory,Profile
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from . forms import UserRegistrationForm,LoginForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib import messages


# register user
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email = userObj['email']
            password = userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')
    else:
        form = UserRegistrationForm()
    return render(request, 'deep_diagnose/register.html', {'form': form})


# for finding companies in a particular area
def home(request):
    return render(request, 'deep_diagnose/user_location.html')


# user profile
@login_required
def profile(request):
    return render(request, 'deep_diagnose/profile.html')


# admin login
def loginAdminPanel(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            if account is not None:
                login(request, account)
                #here is redirecting to admin panel
                return HttpResponseRedirect('/adminhome/')
            else:
                return render(request, 'registration/adminlogin.html')
        else:
            return render(request, 'registration/adminlogin.html')
    else:
        form = LoginForm()
        context = {'form':form}
        return render(request, 'registration/adminlogin.html', context)


# first page for admin
@login_required
def adminhome(request):
    return render(request,'admin/adminhome.html')


# admin profile
@login_required
def adminprofile(request):
    return render(request, 'admin/adminprofile.html')


# for showing result --->companies nearby
def result(request):
    company_list = CompanyDetail.objects.all().order_by('company_name')
    company_filter = CompanyFilter(request.GET, queryset=company_list)
    return render(request, 'deep_diagnose/company_list.html', {'filter': company_filter})


# gives list of all the companies
class CompanyList(generic.ListView):
    template_name = 'deep_diagnose/all_companies.html'
    context_object_name = 'all_companies'

    def get_queryset(self):
        return CompanyDetail.objects.all().order_by('company_name')


# gives details about the company->tests,price,contact info
class CompanyDetails(generic.DetailView):
    template_name = 'deep_diagnose/company_details.html'
    context_object_name = 'company'

    def get_queryset(self):
        return CompanyDetail.objects.all().order_by('test_name')


# delete company
class CompanyDelete(DeleteView):
    model = CompanyDetail
    success_url = reverse_lazy('deep_diagnose:adminhome')


# list of all tests
class TestList(generic.ListView):
    template_name = 'deep_diagnose/all_tests.html'
    context_object_name = 'all_tests'

    def get_queryset(self):
        return Tests.objects.all()


# gives details about selected test
class TestDetail(generic.DetailView):
    model = Tests
    template_name = 'deep_diagnose/test_detail.html'
    context_object_name = 'test'


# test categories
class Category(generic.DetailView):
    model = TestCategory
    template_name = 'deep_diagnose/category.html'
    context_object_name = 'category'


# use another test
class TestCreate(CreateView):
    model = Tests
    fields = ['test_name','category']
    success_url = reverse_lazy('deep_diagnose:adminhome')


# update existing test
class TestUpdate(UpdateView):
    model = Tests
    fields = ['test_name']
    success_url = reverse_lazy('deep_diagnose:adminhome')


# delete test
class TestDelete(DeleteView):
    model = Tests
    success_url = reverse_lazy('deep_diagnose:adminhome')


# returns company name on the basis search item in searchbox
def put_list(request):
    polls = Tests.objects.all()
    search_term=''
    if 'search' in request.GET:
        search_term = request.GET['search']
        polls = polls.filter(test_name__istartswith=search_term)

    context = {'search_term': search_term, 'polls': polls, }
    return render(request, 'deep_diagnose/searchresult.html', context)


def show_results(request, abc):
    # search=request.GET['search']
    polls = CompanyTests.objects.filter(tests__test_name=abc)
    """search_term = ''
    if 'search' in request.GET:
        search_term = request.GET['search']
        polls = polls.filter(test__icontains=search_term)"""

    context = {
        'polls': polls
    }
    return render(request, 'deep_diagnose/base.html', context)


# order the test
class OrderNow(CreateView):
    model = OrderInfo
    template_name = 'deep_diagnose/ordernow.html'
    fields = ['user_name', 'email_id','age','address_line_1','city','state','zip_code','phone_no',
              'suitable_date','suitable_time']
    success_url = reverse_lazy('deep_diagnose:find')


def thankyou(request):
    return render(request, 'deep_Diagnose/thankyou.html')


# gives admin options to delete and update tests
class AdminTestList(generic.ListView):
    template_name = 'admin/admin_test_list.html'
    context_object_name = 'all_tests'

    def get_queryset(self):
        return Tests.objects.all().order_by('test_name')


# show list of companies and admin can delete it
class AdminCompanyList(generic.ListView):
    template_name = 'admin/admin_company_list.html'
    context_object_name = 'all_companies'

    def get_queryset(self):
        return CompanyDetail.objects.all().order_by('company_name')


@login_required
def profile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()

        def redirect_view(request):
            response = redirect('/profile/')
            return response
        # messages.success(request, f'Your Account has been updated')
        # return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'deep_diagnose/profile.html', context)







