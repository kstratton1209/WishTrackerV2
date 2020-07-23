from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from .models import Wishes, Registration


def home(request):
    context = {
        "ungranted_wishes": Wishes.objects.filter(granted = 'False'),
        "granted_wishes": Wishes.objects.filter(granted = 'True')
    }
    return render(request,"home.html", context)

# def wishes(request):
#     context = {

#         }

#     return render(request,"addBook.html", context)


def addWish(request):
    return render(request,"addWish.html")

def createWish(request):
    
    errors = Wishes.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect("/content/addWish")
    else:
        wish_from_form = request.POST['wish']
        description_from_form = request.POST['description']
        user_id = int(request.POST['user_id'])

        logged_user = Registration.objects.get(id = user_id)

        Wishes.objects.create(wish = wish_from_form, description = description_from_form, user = logged_user)

        return redirect('/content/home')

def editWish(request,id):

    context= {
        "wish_id": int(id),
        "wish_details": Wishes.objects.get(id = int(id))
    }
    
    return render(request,"editWish.html", context)



def updateWish(request,id):
    errors = Wishes.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value)
        return redirect(f"/content/{id}/edit")
    else:
        wish_id = int(id)
        new_wish_from_form = request.POST['wish']
        new_description_from_form = request.POST['description']
        
        wish_to_edit = Wishes.objects.get(id=wish_id)

        wish_to_edit.wish = f"{new_wish_from_form}"
        wish_to_edit.description = f"{new_description_from_form}"

        wish_to_edit.save()

        return redirect("/content/home")

def grant(request, id):

    wish_id = int(id)
    wish_to_grant = Wishes.objects.get(id = wish_id)
    wish_to_grant.granted = "True"
    wish_to_grant.save()


    return redirect('/content/home')

    
#     user_id = int(request.POST['user_id'])
#     logged_user = Registration.objects.get(id = user_id)
#     all_wishes = Wishes.objects.all()


#     return render(request,"grantedWishes.html")

def stats(request,id):
    
    user_id = int(id)
    logged_user = Registration.objects.get(id = user_id)

    user_wishes_granted = 0
    for wishes in Wishes.objects.filter(user = logged_user, granted= 'True'):
        user_wishes_granted += 1
    
    user_wishes_ungranted = 0
    for wishes in Wishes.objects.filter(user = logged_user, granted= 'False'):
        user_wishes_ungranted += 1
    
    user_total_wishes = user_wishes_granted + user_wishes_ungranted


    total_wishes = 0
    for wishes in Wishes.objects.filter(granted = 'True'):
        total_wishes += 1

    

    context = {
        "user_wishes_granted": user_wishes_granted,
        "user_wishes_ungranted": user_wishes_ungranted,
        "user_total_wishes": user_total_wishes,
        "total_wishes": total_wishes
    }


    return render(request,"stats.html", context)



def likeWish(request,id):
    wish_id = int(id)
    wish_to_like = Wishes.objects.get(id = wish_id)
    has_this_user_liked = 1

    current_likes = wish_to_like.likes
    new_likes = current_likes + 1

    wish_to_like.likes = new_likes
    wish_to_like.save()
    
    return redirect('/content/home')

def destroyWish(request,id):
    wish_to_delete = Wishes.objects.get(id =int(id))
    wish_to_delete.delete()
    return redirect("/content/home")



