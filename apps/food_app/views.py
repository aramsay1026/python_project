from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from .models import User,Supplier,Shelter,Availability,Feedback
import bcrypt
from datetime import datetime,date,timedelta

def home(request):
    if(not(request.session.get('user_id'))):
<<<<<<< HEAD
	    request.session['user_id']=0
=======
        request.session['user_id']=0
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
    return render(request, 'food_app/index.html')


def validation(request):
    print("I am in validation")
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
<<<<<<< HEAD
        if use.id:
            # request.session['user_type']=request.POST['type']  
=======
        if use.id: 
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
            request.session['user_id']=use.id
            link='/'+request.session['user_type']
            return redirect('/supplier')
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
<<<<<<< HEAD
                    'name':item.shelter_name,       #name of that shelter 
=======
                    'name':this_user.first_name,  
                    'shelter':item.shelter_name,     #name of that shelter 
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
                    'meals':item.meals_required     #no. of meals required by that shelter
                }
                break
     
    
    if flag==False:
        con={
                'shel':User.objects.get(id=18),
<<<<<<< HEAD
                'name':"Food For Everyone",
=======
                'name':this_user.first_name,
                'shelter':"Food for Everyone",
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
                'meals':'50'
            }
    return render(request,"food_app/supplierDeliver.html",con)


def addSupplier(request):
<<<<<<< HEAD
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
=======
    if len(request.POST['numOfFood'])<=0 :
        messages.add_message(request, messages.ERROR, "no. of plates available has to be minimum 10")
        return redirect('/supplier')
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
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
<<<<<<< HEAD
    user=User.objects.get(id=request.session['user_id'])
=======
    user=User.objects.get(id=request.session['user_id'])  # Supplier's object
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
    supplier=Supplier.objects.get(users=user)
    suppliers=Supplier.objects.all()
    shelters=Shelter.objects.all()
    shelter_volunteer=User.objects.exclude(suppliers=suppliers)
    volunteers=shelter_volunteer.exclude(shelters=shelters)
    volunteers_incity=volunteers.filter(city=user.city)       # Volunteers in the supplier's city
    # shelter_user=User.objects.filter(shelters=shelters)
    # shelter_incity=shelter_user.filter(city=user.city)      #shelters in the city where the volunteer and supplier is located
    for item in shelters:    #for every shelter
       use=item.users.all()  #get the user belonging to that shelter
       for us in use:        #for that user find his city
           if us.city == user.city :
               shelter_incity=item.shelter_name
    volunteer_available={}
    for volunteer in volunteers_incity:
        availabilities=volunteer.availabilities.all()
        for availability in availabilities:
            if availability.available_date==supplier.use_by:
                volunteer_available=volunteer
                print volunteer_available
            else:
                print "couldn't assign volunteer"
<<<<<<< HEAD
    if volunteer_available:
        context={
        'volunteer_available':volunteer_available
        }
    else:
        print "sorry no context available"
    return render(request,"food_app/volunteerDeliver.html ",context)
=======

    if volunteer_available:
        context={
        'volunteer_available':volunteer_available,
        'supplier':  user,
        'shelter': shelter_incity
        }
    else:
        context={
            'volunteer_available': User.objects.get(id=18),
            'supplier':user,
            'shelter': "North King County Food Bank"
        }

    #Delete the supllier after his food has been assigned to someone
    Supplier.objects.filter(users=user).delete()
    
    return render(request,"food_app/volunteerDeliver.html",context)
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb

def volunteer_home(request):
    volunteer=User.objects.get(id=request.session['user_id'])

    con_disp={
        'set': volunteer.availabilities.all()
    }

    return render(request,"food_app/volunteer.html",con_disp)

def volunteer_add(request):
    if request.method == "POST":
        volunteer=User.objects.get(id=request.session['user_id'])
        avail=Availability.objects.create(available_date=request.POST['date_available'],available_shift=request.POST['shift'])
        volunteer.availabilities.add(avail)

    return redirect('/volunteers')

def shelter(request):
    return render(request,'food_app/bank.html')
<<<<<<< HEAD

def logout(request):
    request.session.pop('user_id')
    return redirect('/')
=======

def contact(request):
    val = Feedback.objects.all()
    context={
        'message':val
    }
    return render(request,"food_app/contact_us.html",context)

def sendMessage(request):
    Feedback.objects.create(name=request.POST['fname'],email=request.POST['email'],phone=request.POST['phone'],message_description=request.POST['message'])
    return redirect('/contact_us')

def logout(request):
    if request.method == "POST":
        request.session.pop('user_id')

    return redirect('/')

def unjoin(request):
   Availability.objects.get(id=request.POST['action']).delete()
   return redirect('/volunteers')

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

def go_home(request):
    return render(request, "food_app/index.html")

def thankyou(request):
    return render(request, "food_app/thankyou.html")
>>>>>>> 394045ea10d179dfc179842e96c6f5d484304ccb
