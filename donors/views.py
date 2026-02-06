from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import DonorForm
from .models import Donor


# ---------- HOME ----------
def home(request):
    return render(request, 'index.html')


# ---------- AUTH ----------
def signup_view(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        first_time_login = user.last_login is None
        login(request, user)

        if user.is_staff or user.is_superuser:
            return redirect('donor_list')

        if first_time_login:
            return redirect('add_donor')

        return redirect('add_donor')

    return render(request, 'login.html', {'form': form})


# ---------- DONORS ----------
@login_required
def add_donor(request):
    form = DonorForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('donor_list')

    return render(request, 'donor_add.html', {'form': form})



from django.core.paginator import Paginator

@login_required
def donor_list(request):
    if not request.user.is_staff:
        return redirect('home')

    # GET filters
    blood_group = request.GET.get('blood_group', '')
    area = request.GET.get('area', '')

    donors = Donor.objects.all().order_by('-id')

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if area:
        donors = donors.filter(area__icontains=area)

    paginator = Paginator(donors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'donor_list.html', {
        'page_obj': page_obj,
        'blood_group': blood_group,
        'area': area
    })




@login_required
def edit_donor(request, id):
    if not request.user.is_staff:
        return redirect('home')

    donor = get_object_or_404(Donor, id=id)
    form = DonorForm(request.POST or None, instance=donor)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('donor_list')

    return render(request, 'donor_edit.html', {'form': form})


@login_required
def delete_donor(request, id):
    if not request.user.is_staff:
        return redirect('home')

    donor = get_object_or_404(Donor, id=id)
    donor.delete()
    return redirect('donor_list')


@login_required
def search_donors(request):
    if not request.user.is_staff:
        return JsonResponse({'html': ''})

    blood_group = request.GET.get('blood_group', '')
    area = request.GET.get('area', '')
    request.session['blood_group'] = blood_group
    request.session['area'] = area

    donors = Donor.objects.all()

    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    if area:
        donors = donors.filter(area__icontains=area)

    html = render_to_string('partials/donor_rows.html', {'donors': donors})
    return JsonResponse({'html': html})

def kiosk_view(request):
    donors=Donor.objects.all()
    return render(request,'kiosk.html',{'donors':donors})