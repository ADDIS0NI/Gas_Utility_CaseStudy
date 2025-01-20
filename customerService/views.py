from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ServiceRequestForm, UserRegistrationForm, ServiceFeedbackForm
from .models import ServiceRequest, ServiceFeedback
from django.contrib.auth import login
from django.contrib import messages

@login_required
def create_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            messages.success(request, 'Service request submitted successfully!')
            return redirect('track_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'create_request.html', {'form': form})

@login_required
def track_requests(request):
    requests = ServiceRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'track_requests.html', {'requests': requests})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('create_request')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.user = request.user
            service_request.save()
            return redirect('track_requests')
    else:
        form = ServiceRequestForm()
    return render(request, 'submit_request.html', {'form': form})

def home(request):
    if request.user.is_authenticated:
        # Redirect authenticated users to their requests
        return redirect('track_requests')
    return render(request, 'home.html')

def dashboard(request):
    context = {
        'total_requests': ServiceRequest.objects.filter(user=request.user).count(),
        'pending_requests': ServiceRequest.objects.filter(user=request.user, status='pending').count(),
        'completed_requests': ServiceRequest.objects.filter(user=request.user, status='completed').count(),
    }
    return render(request, 'dashboard.html', context)

@login_required
def submit_feedback(request, request_id):
    service_request = get_object_or_404(ServiceRequest, id=request_id, user=request.user)
    
    # Check if feedback already exists
    if ServiceFeedback.objects.filter(service_request=service_request).exists():
        messages.error(request, 'You have already submitted feedback for this request.')
        return redirect('track_requests')
    
    if request.method == 'POST':
        form = ServiceFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.service_request = service_request
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('track_requests')
    else:
        form = ServiceFeedbackForm()
    
    return render(request, 'feedback.html', {
        'form': form,
        'service_request': service_request
    })
