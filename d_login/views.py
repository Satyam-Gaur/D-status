from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,Group

# User forms creation and fetching
from .forms import CreateUserForm, UserDataForm, UserProjectForm, SearchUserForm
from .models import UserData, UserDataHistory, UserProjectData

# login, logout and authentication
from django.contrib.auth import authenticate, login, logout

#downloading to excel
import xlwt
from django.http import HttpResponse


# Create your views here.

def register_user(request):
    form = CreateUserForm()
    context = {}
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        context = {'form': form}
        if form.is_valid():

            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')


            if '@tcs.com' not in email:
                context['d'] = "Please enter your TCS Email Id."
                return render(request,'register.html',context)
            elif password1 != password2:
                context['d'] = "Passwords did not match."
                return render(request,'register.html',context)

            else:
                
                form.save()
                user = User.objects.get(username = form.cleaned_data.get("username"))
                user_data = UserData(user = user)
                data = {}
                data['name'] = user.first_name +' '+ user.last_name
                project_data = UserProjectData(user = user, **data)
                
                user_data.save()
                project_data.save()

                
                messages.success(request, 'Account was created for '+ user.first_name +' :) ')
            
                return redirect('login')
        else:
            pass
    context = {'form' : form}
    return render(request,'register.html',context)
 

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password = password)
            
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.error(request, 'Please enter a valid username and password')
                return redirect('login')
    
    return render(request,'index.html')

@login_required
def home(request):
    user_data = UserData.objects.get(user = request.user)
    
    if request.method == 'POST':
        form = UserDataForm(request.POST)
        if form.is_valid():
            updated_user_data = form.save(commit=False)
            updated_user_data.user = user_data.user
            if updated_user_data.is_next_day(user_data.updated_on):
                update_history(user_data)
            user_data = updated_user_data.save()
    form = UserDataForm()
    user_data = UserData.objects.get(user = request.user)

    fname = User.objects.get(username = user_data.user)

    context = {"form":form, "user_data":user_data,'fname':fname.first_name}
    return render(request,'home.html', context)

def update_history(user_data):
    data = user_data.__dict__
    user = user_data.user
    del data["_state"]
    del data["user_id"]

    hist = UserDataHistory(user = user, **data)
    hist.save()

@login_required
def help(request):
    context = {}
    return render(request,'help.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required
def get_history(request):
    context = get_data(request)

    fname = User.objects.get(username = request.user).first_name

    context["fname"] = fname
    return render(request,"history.html",context)


@login_required
def get_data(request):
    user = request.user
    users_in_group = Group.objects.get(name="admins").user_set.all()
    if user in users_in_group:
        today = UserData.objects.filter()
        hist = UserDataHistory.objects.filter()
        context = {"today" : [i for  i in today]}
        context["hist"] = [i for i in hist]
    else:
        hist = UserDataHistory.objects.filter(user = user)
        today = UserData.objects.filter(user=user)
        context ={"hist": [i for i in hist]}
        context["today"] = [i for i in today]
    
    return context

@login_required
def download_excel_data(request):
        # content-type of response
    response = HttpResponse(content_type='application/ms-excel')

    #decide file name
    response['Content-Disposition'] = 'attachment; filename="status_data.xls"'

    #creating workbook
    wb = xlwt.Workbook(encoding='utf-8')

    #adding sheet
    ws = wb.add_sheet("sheet1")

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    # headers are bold
    font_style.font.bold = True

    #column header names, you can use your own headers here
    columns = ['Emp_Id', 'T-Factor', 'Training', 'Project', 'Status', 'Upcoming Leaves','Updation Date','Updation Time']

    #write column headers in sheet
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/mm/yyyy'

    time_format = xlwt.XFStyle()
    time_format.num_format_str = 'h:mm:ss'
    

    #get your data, from database or from a text file...
    context = get_data(request)

    for my_row in context['hist']:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.user.username, font_style)
        ws.write(row_num, 1, my_row.t_factor, font_style)
        ws.write(row_num, 2, my_row.trainings, font_style)
        ws.write(row_num, 3, my_row.projects, font_style)
        ws.write(row_num, 4, my_row.status, font_style)
        ws.write(row_num, 5, my_row.leaves, font_style)
        ws.write(row_num, 6, my_row.updated_on.date(), date_format)
        ws.write(row_num, 7, my_row.updated_on.time(), time_format)

    for my_row in context['today']:
        row_num = row_num + 1
        ws.write(row_num, 0, my_row.user.username, font_style)
        ws.write(row_num, 1, my_row.t_factor, font_style)
        ws.write(row_num, 2, my_row.trainings, font_style)
        ws.write(row_num, 3, my_row.projects, font_style)
        ws.write(row_num, 4, my_row.status, font_style)
        ws.write(row_num, 5, my_row.leaves, font_style)
        ws.write(row_num, 6, my_row.updated_on.date(), date_format)
        ws.write(row_num, 7, my_row.updated_on.time(), time_format)

    wb.save(response)
    return response


@login_required
def update_project(request):

    user = request.user
    
    users_in_group = Group.objects.get(name="admins").user_set.all()
    if user in users_in_group:

        if request.method == 'POST':
            
            form = UserProjectForm(request.POST)

            if form.is_valid():

                username = form.cleaned_data.get('username')
                project1 = form.cleaned_data.get('project1')
                project2 = form.cleaned_data.get('project2')
                project3 = form.cleaned_data.get('project3')
                project4 = form.cleaned_data.get('project4')
                project5 = form.cleaned_data.get('project5')
                project6 = form.cleaned_data.get('project6')
                project7 = form.cleaned_data.get('project7')
                project8 = form.cleaned_data.get('project8')
                project9 = form.cleaned_data.get('project9')
                project10 = form.cleaned_data.get('project10')
                

                user = UserProjectData.objects.get(user = User.objects.get(username = username))
                
                user.project1 = project1
                user.project2 = project2
                user.project3 = project3
                user.project4 = project4
                user.project5 = project5
                user.project6 = project6
                user.project7 = project7
                user.project8 = project8
                user.project9 = project9
                user.project10 = project10
                
                user.save()
            messages.info(request,'User Project Data Saved')
            return redirect('project_data')


    else:
        messages.error(request,"You don't have required permissions to view the page.")
        return redirect('history')

@login_required
def project_data(request):
    user = request.user
    users_in_group = Group.objects.get(name="admins").user_set.all()
    if user in users_in_group:
        if request.method == 'POST':
            form =  SearchUserForm(request.POST)
            if form.is_valid():

                username = form.cleaned_data.get('username')

                try:
                    user = UserProjectData.objects.get(user = User.objects.get(username = username))
    
                except:
                    messages.error(request,'User not found')
                    return redirect('project_data')

                proj = UserProjectData.objects.all()
                context ={"proj": [i for i in proj]}

                form = UserProjectForm(initial={
                    'username':username,
                    'project1':user.project1,
                    'project2':user.project2,
                    'project3':user.project3,
                    'project4':user.project4,
                    'project5':user.project5,
                    'project6':user.project6,
                    'project7':user.project7,
                    'project8':user.project8,
                    'project9':user.project9,
                    'project10':user.project10
                })
                context['form'] = form
                return render(request,'update_project.html',context)

        proj = UserProjectData.objects.all()
        context ={"proj": [i for i in proj]}

        form = SearchUserForm()
        context['form'] = form
        return render(request,'project_data.html',context)
    else:
        messages.error(request,"You don't have required permissions to view the page.")
        return redirect('history')

