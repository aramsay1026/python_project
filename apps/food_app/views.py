from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import User,Supplier,Shelter,Availability
import bcrypt
from datetime import datetime,date,timedelta

def home(request):
    if(not(request.session.get('user_id'))):
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

          
        use=User.objects.create(first_name=request.POST['first_name'],last_name=request.POST["last_name"],email_address=request.POST['email'],password= passW,address=request.POST['address'],city=request.POST['city'],state="Washington")
        request.session['user_type']=request.POST['type']
        print use
        print "User type"
        print request.session['user_type']
        if use.id:
            # request.session['user_type']=request.POST['type']  
            request.session['user_id']=use.id
            link='/'+request.session['user_type']
            return redirect(link)
        else:
            messages.add_message(request, messages.ERROR, "Could not add new user.. Try again")
            return redirect('/')

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
    print supply
    if supply:
        request.session['user_type']='supplier' 
        return redirect('/supplier')

    else:
        shelter=Shelter.objects.filter(id=request.session['user_id'])
        if shelter:
            request.session['user_type']="bank"
            return redirect('/shelter')
        else: 
            request.session['user_type']="volunteer"
            return redirect('/volunteers')
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


def send_details(request):
    flag=False
    shelts=Shelter.objects.all()   #List of all the Shelters
    this_user=User.objects.get(id=request.session['user_id'])   # The object of supplier of this session
    for item in shelts:    #for every shelter 
        use=item.users.all()  #get the user belonging to that shelter 
        for us in use:        #for that user find his city 
            if us.city == this_user.city :   #Comapre his city to the supplier's city and if yes direct the food to that shelter
                flag=True
                con={
                    'shel':us,                      #list of user belonging to that shelter 
                    'name':item.shelter_name,       #name of that shelter 
                    'meals':item.meals_required     #no. of meals required by that shelter
                }
                break
     
    
    if flag==False:
        con={
                'shel':User.objects.get(id=18),
                'name':"Food For Everyone",
                'meals':'50'
            }
    return render(request,"food_app/supplierDeliver.html",con)


def addSupplier(request):
    print "-------------------------"
    print datetime.today().date()
    print request.POST['cookedOn']
    print "------------------------"
    if len(request.POST['numOfFood'])<=0 :
        messages.add_message(request, messages.ERROR, "no. of plates available has to be minimum 10")
        return redirect('/supplier')
    # elif request.POST['cookedOn'] is '':
    #     print "I am here"
    #     messages.add_message(request, messages.ERROR, "The date cannot be empty")
    #     return redirect('/supplier')
    elif (datetime.today()-timedelta(days=1)).date() > datetime.strptime(request.POST['cookedOn'],"%Y-%m-%d").date():
        messages.add_message(request, messages.ERROR, "The date has to be in future")
        return redirect('/supplier')
    else:
        this_user=User.objects.get(id=request.session['user_id'])
        val=Supplier.objects.create(meals_available=request.POST['numOfFood'],cooked_at=request.POST['cookedOn'],use_by=request.POST['cookedOn'])
    
        this_user.suppliers.add(val)
        
        if request.POST.get('checkDrive',False)=="drive" :
            return redirect('/senddetails')
        else :
            return redirect('/findVolunteer')

def find_volunteer(request):
    user=User.objects.get(id=request.session['user_id'])
    supplier=Supplier.objects.get(users=user)
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
            if availability.available_date==supplier.use_by:
                volunteer_available=volunteer
                print volunteer_available
            else:
                print "couldn't assign volunteer"
    if volunteer_available:
        context={
        'volunteer_available':volunteer_available
        }
    else:
        print "sorry no context available"
    return render(request,"food_app/volunteerDeliver.html ",context)

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
    return render(request,'food_app/bank.html')


