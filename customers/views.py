from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from customers.models import Client, Domain

def is_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser)
def saas_dashboard(request):
    clients = Client.objects.all().order_by('-created_on')
    
    # Simple stats
    total_clients = clients.count()
    active_trials = clients.filter(on_trial=True).count()
    
    context = {
        'clients': clients,
        'total_clients': total_clients,
        'active_trials': active_trials,
    }
    return render(request, 'saas_dashboard.html', context)
