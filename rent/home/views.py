from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.generic import View, DetailView
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
from .models import VehicleAvailable, UserAvailable,ItemsOrdered,Renter
from django.db.models import Q
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
# from twilio.rest import Client




# Create your views here.

class BaseView(View):
    template_context = {

    }


class IndexView(BaseView):
    def post(self, request):
        return render(request, 'index.html')

    def get(self, request):
        return render(request, 'index.html', self.template_context)


class LoginView(BaseView):
    def post(self, request):
        if self.request.method == 'POST' and 'go_btn' in self.request.POST:
            username = self.request.POST.get('UserName')
            password = self.request.POST.get('Password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(self.request, user)
                return render(request, 'index.html', self.template_context)
            else:
                messages.error(request,'Login Failed')
        return render(request, 'login.html', self.template_context)

    def get(self, request):
        return render(request, 'login.html', self.template_context)


class SignupView(BaseView):
    def post(self, request):
        if 'signup_btn' in self.request.POST:
            username = self.request.POST.get('UserName')
            email = self.request.POST.get('Email')
            password = self.request.POST.get('Password')
            confirmpassword = self.request.POST.get('ConfirmPassword')
            if (confirmpassword == password):
                if User.objects.filter(username=username).exists():
                    messages.error(request, "This username is already taken")
                    return redirect('home:signup')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "This email is already taken")
                    return redirect('home:signup')
                else:
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
        return render(request, 'login.html')

    def get(self, request):
        return render(request, 'registration.html')


class Available(BaseView): #/available
    def get(self,request):
        self.template_context['avehicles'] = VehicleAvailable.objects.all()
        query = request.GET.get('query')
        if query is not None and query != '':
            self.template_context['search_result'] = VehicleAvailable.objects.filter(
                Q(type__icontains=query)| Q(model__icontains=query) |Q(manufacturer_company__startswith=query)|
                Q(manufacturer_company__endswith=query)
            )
            self.template_context['search_for'] = query
            return render(request, 'search-list.html', self.template_context)
        else:
            return render(request,'car-list-two.html',self.template_context)


class RentVehicles(View):# /rent
    def post(self, request):
        username = self.request.POST.get('UserName')
        password = self.request.POST.get('Password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            username = request.user
            code=request.POST.get('code')
            codecheck=get_object_or_404(Renter, autocode=code)
            manufacturer = request.POST.get('manufacturer')
            image = request.POST.get('image')
            model = request.POST.get('model')
            type = request.POST.get('type')
            pph = request.POST.get('pph')
            pickup = request.POST.get('pickuploc')
            drop = request.POST.get('droploc')
            time = request.POST.get('time')
            date = request.POST.get('date')
            description = request.POST.get('description')
            km = request.POST.get('km')
            # slug=manufacturer+"-"+model+"-"+type+"-"+value
            availvech = VehicleAvailable.objects.create(
                user=username,
                vech_owner=codecheck,
                type =type,
                manufacturer_company = manufacturer,
                model = model,
                pickup = pickup,
                dropup = drop,
                available_till_time = time,
                available_till_date = date,
            # special_rating=models.BooleanField(default=0),
                description = description,
                image = image,
                priceph = pph,
                km_travelled = km,
                # slug=slug,
                ordered=False,
            )
            availvech.save()
            return render(request, 'home-two.html')
        else:
            messages.error(request, 'Login First')
            return render(request, 'login.html')

    def get(self,request):
        return render(request, 'home-two.html')

class Reservation(BaseView):
    def get(self, request):
        return render(request, 'reservation.html', self.template_context)


class ReservationDetailView(DetailView):
    model = VehicleAvailable
    template_name = 'reservation.html'

    def post(self, request,slug):
        if request.user is not None:
            username = request.user
            phone = request.POST.get('phone')
            location = request.POST.get('location')
            description = request.POST.get('description')
            item = get_object_or_404(VehicleAvailable, slug=slug)
            renter_details=get_object_or_404(Renter,autocode=item.vech_owner.autocode)
            ordervech = UserAvailable.objects.create(
                # items=item,
                user=username,
                phone=phone,
                location=location,
                renter_details=renter_details,
                ordered=True,
                info=description
            )
            ordervech.items.add(item)
            # ordervech.items.add(renter_details)
            ordervech.save()
            store_item = ItemsOrdered.objects.create(
                user=username,
                item=item,
                orderedfrom=renter_details,
                ordered=True,
                free=False,
            )
            store_item.save()

            return render(request, 'index.html')
        else:
            messages.error(request,"Please Login First")
            return redirect(reverse('home:login'))