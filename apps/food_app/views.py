from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import User,Supplier,Shelter,Availability
import bcrypt
from datetime import datetime,date,timedelta

def home(request):
	request.session['user_id']=0
	return render(request, 'food_app/index.html')


def validation(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
           messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        passW= bcrypt.hashpw(request.POST['psw'].encode(), bcrypt.gensalt())
        check=User.objects.all()
        for item in check:
            if item.email_address==request.POST['email']:
                messages.add_message(request, messages.ERROR, "User Already exists.. Please login")
                print item.email_address
                print "User Already Exists"
                return redirect('/')
            
        use=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST["last_name"],email_address=request.POST['email'],password= passW,address=request.POST['address'],city=request.POST['city'],state="Wshington")
        if use.id:
            request.session['user_id']=use.id
            return redirect('/sendtosuccess')
        else:
            messages.add_message(request, messages.ERROR, "Could not add new user.. Try again")

def login(request):
    log=User.objects.all()
    for value in log:
        if value.email_address==request.POST['email'] and bcrypt.checkpw(request.POST['psw'].encode(), value.password.encode()):
            request.session['user_id']=value.id
            return redirect('/sendtosuccess') 

    messages.add_message(request, messages.ERROR, "Something went wrong..check your id & password")
    return redirect('/')

def process(request):
    user_details=User.objects.get(id=request.session['user_id'])
    supply=Supplier.objects.filter(id=request.session['user_id'])

    if not supply :
        shelter=Shelter.objects.filter(id=request.session['user_id'])
        if not shelter :
            request.session['user_type']="Volunteer"
            return redirect('/volunteers')
        else: 
            request.session['user_type']="Shelter"
            return redirect('/shelter')
    else:
        request.session['user_type']='Supplier' 
        return redirect('/supplier') 

    context={
        'name':user_details.first_name
    }
    return render(request, 'food_app/stage.html',context)

def supplier(request):
	user_details=User.objects.get(id=request.session['user_id'])
	context={
		'name':user_details.first_name
	}
	return render(request,'food_app/supplier.html',context)

def addSupplier(request):
    if int(request.POST['numOfFood'])<=0 :
        messages.add_message(request, messages.ERROR, "no. of plates available has to be minimum 10")
    this_user=User.objects.get(id=request.session['user_id'])
    print "----------"
    print this_user.first_name
    print "----------"
    val=Supplier.objects.create(meals_available=request.POST['numOfFood'],cooked_at=request.POST['cookedOn'], use_by=request.POST['cookedOn'])
    val.users.add(this_user)
    print "*********************************"
    print request.POST.get('checkDrive',False)
    print "**********************************"
    if request.POST.get('checkDrive',False)=="drive" :
        return redirect('/senddetails')
    else :
        return redirect('/findVolunteer')

def send_details(request):
    flag=False
    shelts=Shelter.objects.all()
    this_user=User.objects.get(id=request.session['user_id'])
    for item in shelts:
        use=item.users.all()
        for us in use:
            if us.city == this_user.city :
                flag=True
                con={
                    'shel':us,
                    'name':item.shelter_name,
                    'meals':item.meals_required
                }
        

    if flag==False:
        con={
        'shel':'',
        'name':this_user.first_name,
        'meals':'45'
        }

    
        # else :
        #     con={
        #         'shel':shelts
        #         'val':
        #     }
    return render(request,"food_app/supplierDeliver.html",con)

def find_volunteer(request):
    user=User.objects.get(id=request.session['user_id'])
    supplier=Supplier.objects.get(id=user.id)
    suppliers=Supplier.objects.all()
    shelters=Shelter.objects.all()
    shelter_volunteer=User.objects.exclude(suppliers=suppliers)
    volunteers=shelter_volunteer.exclude(shelters=shelters)
    volunteers_incity=volunteers.filter(city=user.city)
    print "---------------"
    print volunteers_incity
    print "----------------"
    volunteer_available={}
    for volunteer in volunteers_incity:
        availabilities=volunteer.availabilities.all()
        for availability in availabilities:
            if availability.available_date<=supplier.use_by:
                volunteer_available=volunteer
    context={
        'volunteer_available':volunteer_available,
        'name':user.first_name
    }
    return render(request,"food_app/volunteerDeliver.html",context)

def volunteer_home(request):
    volunteer=User.objects.get(id=request.session['user_id'])

    con_disp={
        'set': volunteer.availabilities.all()
    }

    # print "---------------"
    # print con_disp['set']
    # print "----------------"
    return render(request,"food_app/volunteer.html",con_disp)

def volunteer_add(request):
    volunteer=User.objects.get(id=request.session['user_id'])
    print "Hey Hey Hey Hey "
    avail=Availability.objects.create(available_date=request.POST['date_available'],available_shift=request.POST['shift'])
    print "-------------------"
    print volunteer.id, avail
    print "-----------Hey--------"
    volunteer.availabilities.add(avail)

    return redirect('/volunteers')

def shelter(request):
    return HttpResponse("Hey ")

def about(request):
    return render(request, "food_app/about.html")

def about_shelters(request):
    return render(request, "food_app/about_shelters.html")

def about_suppliers(request):
    return render(request, "food_app/about_suppliers.html")

def about_volunteers(request):
    return render(request, "food_app/about_volunteers.html")

def about_team(request):
    return render(request, "food_app/about_team.html")

def contact_us(request):
    return render(request, "food_app/contact_us.html")