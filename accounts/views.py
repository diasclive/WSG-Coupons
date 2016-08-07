from .forms import PersonCreationForm
from django.shortcuts import redirect, render

def register(request):
    if request.method == 'POST':
        form = PersonCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
    else:
        form = PersonCreationForm()
    return render(request, 'registration/register.html', {'form':form})
