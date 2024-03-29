from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.views.generic import View, DetailView, RedirectView
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
from rest_framework.reverse import reverse_lazy

from .models import VehicleAvailable, UserAvailable,ItemsOrdered
from django.db.models import Q
from django.shortcuts import reverse
from django.contrib.auth.decorators import login_required
# from twilio.rest import Client

from .forms import ConsultaionForm


# Create your views here.

class BaseView(View):
    #context variable ho template ma value pathuxa
    template_context = {

    }

class IndexView(BaseView): #home
    def post(self, request):
        form = ConsultaionForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request,'Invalid Entries')
        return render(request, 'index.html',self.template_context)

    def get(self, request):
        form = ConsultaionForm()
        self.template_context['form'] = form
        return render(request, 'index.html', self.template_context)

class LogoutView(RedirectView):# logout paxi home page ma janey
    url = reverse_lazy('home:home')

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)


class LoginView(BaseView): #login garney
    def post(self, request):
        if self.request.method == 'POST' and 'go_btn' in self.request.POST:
            username = self.request.POST.get('UserName')
            password = self.request.POST.get('Password')
            user = auth.authenticate(username=username, password=password) #authenticate garxa
            if user is not None:
                auth.login(self.request, user) #login
                return render(request, 'index.html', self.template_context) #home page ma janx
            else:
                messages.error(request,'Login Failed')
        return render(request, 'login.html', self.template_context)

    def get(self, request):
        # print(request.user)
        if request.user.is_authenticated:
            return redirect('home:home')
        else:
            return render(request, 'login.html', self.template_context)

class SignupView(BaseView): #signup garxa
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
                    user.save() # new user banxa
        return redirect('home:login')

    def get(self, request):
        return render(request, 'registration.html')


class Available(BaseView): #/available  #sell all vehicle available
    def get(self,request):
        self.template_context['avehicles'] = VehicleAvailable.objects.all()
        query = request.GET.get('query')
        if query is not None and query != '': #search
            self.template_context['search_result'] = VehicleAvailable.objects.filter(
                Q(type__icontains=query)| Q(model__icontains=query) |Q(manufacturer_company__startswith=query)|
                Q(manufacturer_company__endswith=query)
            )
            self.template_context['search_for'] = query
            return render(request, 'search-list.html', self.template_context)
        else:
            return render(request,'car-list-two.html',self.template_context)


class RentVehicles(View):# /rent # rent ko form lagi
    def post(self, request):
        username = self.request.POST.get('UserName')
        password = self.request.POST.get('Password')
        user = auth.authenticate(username=username, password=password)
        if request.user.is_authenticated:
            username = request.user
            code=request.POST.get('code')
            # codecheck=get_object_or_404(Renter, autocode=code)
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
            terms = request.POST.get('terms')
            slug=manufacturer+"-"+model+"-"+type+"-"+date
            availvech = VehicleAvailable.objects.create(
                user=username,
                # vech_owner=codecheck,
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
                slug=slug,
                ordered=False,
                terms = terms
            )
            availvech.save()
            return render(request, 'home-two.html')
        else:
            messages.error(request, 'Login First')
            return render(request, 'login.html')

    def get(self,request):
        return render(request, 'home-two.html')

class Reservation(BaseView): # reservation page ko lagi
    def get(self, request):
        return render(request, 'reservation.html', self.template_context)


class ReservationDetailView(DetailView): #reservation ko detail view
    model = VehicleAvailable
    template_name = 'reservation.html'
    def get(self,request,slug):
        if not request.user.is_authenticated:
            messages.error(request, "Please Login First")
            return redirect(reverse('home:login'))
        return super(ReservationDetailView, self).get(request,slug)

    def post(self, request,slug):
        if request.user.is_authenticated:
            username = request.user
            phone = request.POST.get('phone')
            if phone == '' and phone==str:
                messages.error(request, "Invalid Phone Number ")
                return redirect('home:reservation', slug=slug)
            location = request.POST.get('location')
            description = request.POST.get('description')
            terms = request.POST.get('terms')
            item = get_object_or_404(VehicleAvailable, slug=slug)
            if not terms:
                messages.error(request, "Please Accept Term And Conditions ")
                return redirect('home:reservation', slug=slug)
            # renter_details=get_object_or_404(Renter,autocode=item.vech_owner.autocode)
            ordervech = UserAvailable.objects.create(
                # items=item,
                user=username,
                phone=phone,
                location=location,
                # renter_details=renter_details,
                approved=False,
                info=description
            )
            ordervech.items.add(item)
            # ordervech.items.add(renter_details)
            ordervech.save()
            store_item = ItemsOrdered.objects.create(
                user=username,
                item=item,
                # orderedfrom=renter_details,
                ordered=True,
                terms=terms,
            )
            store_item.save()
            return redirect('home:home')
        else:
            messages.error(request,"Please Login First")
            return redirect(reverse('home:login'))

class Profile(BaseView): #/profile  #hirer ko profile display
    def get(self,request):
        self.template_context['ovehicles'] = UserAvailable.objects.filter(user__id = self.request.user.id)
        query = request.GET.get('query')
        if query is not None and query != '':
            self.template_context['search_result'] = VehicleAvailable.objects.filter(
                Q(type__icontains=query)| Q(model__icontains=query) |Q(manufacturer_company__startswith=query)|
                Q(manufacturer_company__endswith=query)
            )
            self.template_context['search_for'] = query
            return render(request, 'search-list.html', self.template_context)
        else:
            return render(request,'hire-profile.html',self.template_context)

    def post(self,request,slug):
    #     print(slug)
        get_vech = VehicleAvailable.objects.get(slug = slug)
        print("xxxxxx")
        print(get_vech)
        print("xxxxxx")

        if 'cmn-btn' in self.request.POST:
            UserAvailable.objects.get ( items = get_vech , user= request.user  ).delete()
            return redirect('home:profile')


class UpdateOrder(BaseView): #edit order
    def get(self,request,slug):
        get_vech = VehicleAvailable.objects.filter(slug=slug)[0]
        user_detail = VehicleAvailable.objects.get(slug=slug)
        self.template_context['userdetail'] = user_detail
        self.template_context['hirer'] = UserAvailable.objects.get(items=get_vech,user = request.user)
        return render(request, 'reservation-update.html', self.template_context)

    def post(self,request, slug):
        print("post")
        get_vech = VehicleAvailable.objects.filter(slug=slug)
        user_detail = VehicleAvailable.objects.get(slug=slug)
        self.template_context['userdetail'] = user_detail
        self.template_context['hirer'] = UserAvailable.objects.get(items=get_vech)
        user_avail_update = UserAvailable.objects.get(items=get_vech, user = request.user)
        user_avail_update.phone = request.POST.get('phone')
        user_avail_update.location = request.POST.get('location')
        user_avail_update.description = request.POST.get('description')
        user_avail_update.save()
        return redirect('home:profile')

class RenterProfile(BaseView): #renter ko profile
    def get(self,request):
        self.template_context['rentvehicles'] = VehicleAvailable.objects.filter(user=self.request.user)
        vehicle_req = VehicleAvailable.objects.filter(user = request.user )
        print(vehicle_req)
        try:
            self.template_context ['requests'] = UserAvailable.objects.filter(items = vehicle_req[0])
        except IndexError:
            self.template_context['requests'] = UserAvailable.objects.filter(items=vehicle_req)
        self.template_context['approvedcount'] = UserAvailable.objects.filter(approved=True)
        # print(self.template_context['rentvehicles'])
        print("+++++++++++++++++++CCCCCCCCCCC")
        query = request.GET.get('query')
        if query is not None and query != '':
            self.template_context['search_result'] = VehicleAvailable.objects.filter(
                Q(type__icontains=query) | Q(model__icontains=query) | Q(manufacturer_company__startswith=query) |
                Q(manufacturer_company__endswith=query)
            )
            self.template_context['search_for'] = query
            return render(request, 'search-list.html', self.template_context)
        return render(request,'rent-profile.html',self.template_context)

    def post(self, request, slug):
        #     print(slug)
        get_vech = VehicleAvailable.objects.get(slug=slug)
        UserAvailable.objects.get(items=get_vech,user = request.user).delete()
        return redirect('home:renter-profile')

class RenterApproval(BaseView):   #renter ko profile ma kati ota hirer ko request aako xa dekhauney
    def get(self,request,slug):
        ordered_vehicle = VehicleAvailable.objects.get(slug = slug, user = request.user)
        self.template_context['orderedfrom'] = UserAvailable.objects.filter(items = ordered_vehicle)
        self.template_context['approvedcount'] = UserAvailable.objects.filter(approved = True)
        return render(request, 'rent-approve-reservation.html',self.template_context )


class RenterAprovalFixOrder(BaseView):#hirer ko request approve garney
    def post(self,request,slug,user_id):
        get_vech = VehicleAvailable.objects.get(slug=slug)
        if 'approve-btn-service' in request.POST:
            ordered_user = UserAvailable.objects.get(items= get_vech,user__id=user_id)
            print("---------------------------------------------")
            # print(ordered_user)
            ordered_user.approved = True
            # ordered_user.rejected = False
            ordered_user.save()
            return redirect('home:renter-profile')
        if 'reject-rent-cmn-btn' in request.POST:
            ordered_user = UserAvailable.objects.get(items = get_vech,user__id=user_id)
            print(ordered_user)
            ordered_user.approved = False
            # ordered_user.rejected = True
            ordered_user.save()
            return redirect('home:renter-profile')
            

class About(BaseView):
    def get(self,request):
        return render(request,'about.html')

class Contact(BaseView):
    def get(self,request):
        return render(request,'contact.html')

class Terms(BaseView):
    def get(self,request):
        return render(request,'terms.html')