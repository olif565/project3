from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

from account.forms import SignUpForm


class IndexView(ListView):
    template_name = 'home_data_user.html'
    context_object_name = 'data_list'

    def get_queryset(self):

        db = User.objects.all()

        data_list = []

        status = {
            True: 'Admin',
            False: 'Staff'
        }

        for x in db:
            data = {
                'pk': int(x.pk),
                'username': x.username,
                'first_name': x.first_name,
                'last_name': x.last_name,
                'email': x.email,
                'status': status.get(x.is_superuser)
            }
            data_list.append(data)

        context = {
            'dt': data_list
        }

        return context


class DataDetailView(DetailView):
    model = User
    template_name = 'home_data_user_detail.html'


def detail(request, pk, template_name='home_data_user_detail.html'):
    db = get_object_or_404(User, pk=pk)

    if db is not None:
        status = {
            True: 'Admin',
            False: 'Staff'
        }
        profile = {
            'username': db.username,
            'first_name': db.first_name,
            'last_name': db.last_name,
            'email': db.email,
            'status': status.get(db.is_superuser)
        }
    else:
        profile = {
            'username': '-',
            'first_name': '-',
            'last_name': '-',
            'email': '-',
            'status': '-'
        }

    context = {
        'profile': profile
    }

    return render(request, template_name, context)


def create(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = form.save()
                user.refresh_from_db()
                user.username = form.cleaned_data.get('username')
                user.first_name = form.cleaned_data.get('first_name')
                user.last_name = form.cleaned_data.get('last_name')
                user.email = form.cleaned_data.get('email')

                if form.cleaned_data.get('is_staff') == 'True':
                    user.is_superuser = True
                    user.is_staff = False
                else:
                    user.is_superuser = False
                    user.is_staff = True

                user.save()

                return redirect('home:data-user')

    form = SignUpForm()
    return render(request, 'home_data_user_create.html', {'form': form})


def edit(request, pk, template_name='home_data_user_edit.html'):
    data = get_object_or_404(User, pk=pk)
    form = SignUpForm(request.POST or None, instance=data)

    if form.is_valid():
        if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
            user = form.save()
            user.refresh_from_db()
            user.username = form.cleaned_data.get('username')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')

            if form.cleaned_data.get('is_staff') == 'True':
                user.is_superuser = True
                user.is_staff = False
            else:
                user.is_superuser = False
                user.is_staff = True

            user.save()

        return redirect('home:data-user')

    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='confirm_delete.html'):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('home:data-user')
    return render(request, template_name, {'object': user})

