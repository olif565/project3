from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, DetailView
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from home.models import Data
from home.forms import DataForm


def dashboard(request):
    if 'username' in request.session:
        return render(request, 'home.html', {})
    else:
        return redirect('/')


class IndexView(ListView):
    template_name = 'home_data_training.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        return Data.objects.all()


class DataDetailView(DetailView):
    model = Data
    template_name = 'home_data_training_detail.html'


def detail(request, pk, template_name='home_data_training_detail.html'):
    data = get_object_or_404(Data, pk=pk)
    return render(request, template_name, data)


def create(request):
    form = DataForm()

    if request.method == 'POST':
        if request.POST.get("input_excel"):
            try:
                excel_file = request.FILES['file-excel']
            except MultiValueDictKeyError:
                return render(request, 'home_data_training_create.html', {'form': form})

            if str(excel_file).split('.')[-1] == 'xls':
                data = xls_get(excel_file, column_limit=5)
            elif str(excel_file).split('.')[-1] == 'xlsx':
                data = xlsx_get(excel_file, column_limit=5)
            else:
                return render(request, 'home_data_training_create.html', {'form': form})

            if data is not None:
                save_excel_to_db(data)
                return redirect('home:data-training')
        else:
            form = DataForm(request.POST)
            if form.is_valid():
                no = form.cleaned_data['no']
                ppm_ch4 = float(form.cleaned_data['ppm_ch4'])
                ppm_c2h4 = float(form.cleaned_data['ppm_c2h4'])
                ppm_c2h2 = float(form.cleaned_data['ppm_c2h2'])
                fault = form.cleaned_data['fault']

                sum = ppm_ch4 + ppm_c2h4 + ppm_c2h2
                ch4 = (ppm_ch4 / sum) * 100
                c2h4 = (ppm_c2h4 / sum) * 100
                c2h2 = (ppm_c2h2 / sum) * 100

                try:
                    param = Data.objects.get(no=no)
                except Data.DoesNotExist:
                    param = Data()
                    param.no = no

                param.ppm_ch4 = ppm_ch4
                param.ppm_c2h4 = ppm_c2h4
                param.ppm_c2h2 = ppm_c2h2
                param.persen_ch4 = ch4
                param.persen_c2h4 = c2h4
                param.persen_c2h2 = c2h2
                param.fault = fault
                param.save()

                return redirect('home:data-training')

    return render(request, 'home_data_training_create.html', {'form': form})


def edit(request, pk, template_name='edit.html'):
    data = get_object_or_404(Data, pk=pk)
    form = DataForm(request.POST or None, instance=data)
    if form.is_valid():

        no = form.cleaned_data['no']
        ppm_ch4 = float(form.cleaned_data['ppm_ch4'])
        ppm_c2h4 = float(form.cleaned_data['ppm_c2h4'])
        ppm_c2h2 = float(form.cleaned_data['ppm_c2h2'])
        fault = form.cleaned_data['fault']

        sum = ppm_ch4 + ppm_c2h4 + ppm_c2h2
        ch4 = (ppm_ch4 / sum) * 100
        c2h4 = (ppm_c2h4 / sum) * 100
        c2h2 = (ppm_c2h2 / sum) * 100

        try:
            param = Data.objects.get(no=no)
        except Data.DoesNotExist:
            param = Data()
            param.no = no

        param.ppm_ch4 = ppm_ch4
        param.ppm_c2h4 = ppm_c2h4
        param.ppm_c2h2 = ppm_c2h2
        param.persen_ch4 = ch4
        param.persen_c2h4 = c2h4
        param.persen_c2h2 = c2h2
        param.fault = fault
        param.save()

        return redirect('home:data-training')

    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='confirm_delete.html'):
    contact = get_object_or_404(Data, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('home:data-training')
    return render(request, template_name, {'object': contact})


def logout_view(request):
    logout(request)
    return redirect('/')


def save_excel_to_db(data_excel):
    for d_sheet in data_excel:
        sheet = data_excel[d_sheet]
        if len(sheet) > 1:  # data sheet
            for data in sheet:
                if len(data) > 0:  # check row tidak kosong
                    if str(data[0]).lower() != 'no':  # check bukan header

                        # Check jika ada data yg kosong
                        if len(data) < 5:
                            i = len(data)
                            while i < 5:
                                data.append('')
                                i += 1

                        # Simpan data
                        no = data[0]
                        db = Data.objects.filter(no=str(no))

                        sum = float(data[1])+float(data[2])+float(data[3])
                        ch4 = (data[1] / sum) * 100
                        c2h4 = (data[2] / sum) * 100
                        c2h2 = (data[3] / sum) * 100

                        if len(db) == 0:
                            Data.objects.create(
                                no=data[0],
                                ppm_ch4=data[1],
                                ppm_c2h4=data[2],
                                ppm_c2h2=data[3],
                                persen_ch4=ch4,
                                persen_c2h4=c2h4,
                                persen_c2h2=c2h2,
                                fault=data[4]
                            )
                        else:
                            dt = db[0]
                            dt.no = data[0]
                            dt.ppm_ch4 = data[1]
                            dt.ppm_c2h4 = data[2]
                            dt.ppm_c2h2 = data[3]
                            dt.persen_ch4 = ch4
                            dt.persen_c2h4 = c2h4
                            dt.persen_c2h2 = c2h2
                            dt.fault = data[4]
                            dt.save()
