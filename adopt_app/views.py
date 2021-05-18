from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if User.objects.filter(user_email = request.POST['user_email']):
            messages.error(request, "Email is already registered")
            return redirect('/')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            user_affiliation = request.POST['user_affiliation'],
            user_email = request.POST['user_email'],
            user_address = request.POST['user_address'],
            user_city = request.POST['user_city'],
            user_state = request.POST['user_state'],
            user_zipcode = request.POST['user_zipcode'],
            password = hash_pw,
        )
        request.session['logged_user'] = new_user.id
        messages.success(request, "User successfully created")
        return redirect('/dashboard')
    return redirect("/")

def login(request):
    return render(request, 'signin.html')

def signin(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            logged_user = User.objects.get(user_email = request.POST['user_email'])
            request.session['logged_user'] = logged_user.id
            return redirect('/dashboard')
    return redirect("/")

def dashboard(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    user = User.objects.get(id=request.session['logged_user'])

    context = {
        'logged_user': user,
        'pets': Pet.objects.all(),
        'feature': Pet.objects.filter(status='At a Kill Shelter'),
        'status': Pet.objects.exclude(status='Adopted') and Pet.objects.exclude(status='Pending'),
    }

    longest_pet = Pet.objects.order_by('created_by')
    longest_available = longest_pet.filter(status="Available")

    return render(request, 'dashboard.html', context, {'longest_available': longest_available})

def logout(request):
    request.session.flush()
    messages.error(request, "You have successfully logged out")
    return redirect('/')

def newpet(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    
    if request.method == "POST":
        errors = Pet.objects.pet_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_pet')
        
        user = User.objects.get(id=request.session['logged_user'])
        
        # context = {}
        # if request.method == "POST":
        #     form = PetForm(request.POST, request.FILES)
        #     context['form'] = form

        # return render(request, "add_pet.html", context)
        pet = Pet.objects.create(
            name=request.POST['name'],
            animal=request.POST['animal'],
            age=request.POST['age'],
            sex=request.POST['sex'],
            pet_city=request.POST['pet_city'],
            pet_state=request.POST['pet_state'],
            pet_zip_code=request.POST['pet_zip_code'],
            pet_affiliation=request.POST['pet_affiliation'],
            description=request.POST['description'],
            photo=request.FILES['photo'],
            status=request.POST['status'],
            created_by=User.objects.get(id=request.session['logged_user'])
        )
        
        return redirect('/dashboard')

    return redirect('/dashboard')


def add_pet(request):

    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    user = User.objects.get(id=request.session['logged_user'])

    context = {
        'logged_user': user,
        'pets': Pet.objects.all()
    }
    return render(request, 'add_pet.html', context)

def pet(request, id):
    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'pet': Pet.objects.get(id=id),
    }
    return render(request, 'pet.html', context)

def edit_form(request, id):
    
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'pet': Pet.objects.get(id=id),
    }
    return render(request, 'edit_pet.html', context)

def edit_pet(request, id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    
    if request.method == "POST":
        errors = Pet.objects.pet_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect(f'/pets/edit/{id}')

        update_pet = Pet.objects.get(id=id)
        update_pet.name=request.POST['name']
        update_pet.animal=request.POST['animal']
        update_pet.age=request.POST['age']
        update_pet.sex=request.POST['sex']
        update_pet.pet_city=request.POST['pet_city']
        update_pet.pet_state=request.POST['pet_state']
        update_pet.pet_zip_code=request.POST['pet_zip_code']
        update_pet.pet_affiliation=request.POST['pet_affiliation']
        update_pet.description=request.POST['description']
        # update_pet.photo=request.FILES['photo']
        update_pet.status=request.POST['status']
        update_pet.save()
        return redirect('/dashboard')

    return redirect('/dashboard')

def delete_pet(request, id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    delete_pet = Pet.objects.get(id=id)
    delete_pet.delete()
    return redirect('/dashboard')

def favorite(request, id):
    current_pet = Pet.objects.get(id=id)
    user_favoriting = User.objects.get(id=request.session['logged_user'])
    current_pet.user_fav.add(user_favoriting)
    return redirect('/dashboard')

def account(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    user = User.objects.get(id=request.session['logged_user'])

    context = {
        'logged_user': user,
        'pets': Pet.objects.all(),
        'adoptpet': Pet.objects.filter(user_adopt=request.session['logged_user'])
    }
    return render(request, 'account.html', context)

def adopt_form(request, id):
    
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')

    context = {
        'logged_user': User.objects.get(id=request.session['logged_user']),
        'pet': Pet.objects.get(id=id),
    }
    return render(request, 'adopt.html', context)

def adopt_pet(request, id):
    if 'logged_user' not in request.session:
        messages.error(request, "Please register or log in first!")
        return redirect('/')
    
    if request.method == "POST":
        errors = Adopt.objects.adopt_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect(f'/pets/edit/{id}')

        adopt = Adopt.objects.create(
            adopt_fname=request.POST['adopt_fname'],
            adopt_lname=request.POST['adopt_lname'],
            adopt_email=request.POST['adopt_email'],
            adopt_address=request.POST['adopt_address'],
            adopt_city=request.POST['adopt_city'],
            adopt_state=request.POST['adopt_state'],
            adopt_zipcode=request.POST['adopt_zipcode'],
            home=request.POST['home'],
            other_pets=request.POST['other_pets'],
            children=request.POST['children'],
        )

        update_status = Pet.objects.get(id=id)
        update_status.status='Pending'
        user_adopting = User.objects.get(id=request.session['logged_user'])
        update_status.user_adopt.add(user_adopting)
        update_status.save()
        return redirect('/dashboard')

    return redirect('/dashboard')

# def get_context_data(self, **kwargs):
#     context = super().get_context_data(**kwargs)
#     context['filter'] = PetFilter(self.request.GET, queryset=self.get_queryset())
#     return context