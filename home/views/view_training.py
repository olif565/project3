from django.shortcuts import render
from django.views.generic import ListView

from home.forms import ParameterForm
from home.models import Parameter
from home.views import training, normalisasi
import logging

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'home_training.html'
    context_object_name = 'data'

    def get_queryset(self, **kwargs):

        try:
            data = Parameter.objects.get(id='1')
            if data is None:
                form = ParameterForm()
                lamda = None
                complexity = None
                gamma = None
                iterasi = None
                s = '2'
            else:
                l = data.lamda
                c = data.complexity
                g = data.gamma
                i = data.iterasi
                s = data.sigma

                if l is None or not s.strip():
                    l = '1'
                if c is None or not s.strip():
                    c = '0.1'
                if g is None or not s.strip():
                    g = '1'
                if i is None or not s.strip():
                    i = '10'
                if s is None or not s.strip():
                    s = '2'

                lamda = float(l)
                complexity = float(c)
                gamma = float(g)
                iterasi = int(i)

                form = ParameterForm(initial={
                    'lamda': data.lamda,
                    'complexity': data.complexity,
                    'gamma': data.gamma,
                    'iterasi': data.iterasi
                })
        except Parameter.DoesNotExist:
            form = ParameterForm()
            lamda = None
            complexity = None
            gamma = None
            iterasi = None
            s = '2'

        level = self.kwargs['level']

        n_data_normalisasi = []
        n_list_data_matriks_view = []
        data_iterasi = []
        data_bobot = []
        bias = 0

        if level == 1:
            display_form = 'block'
            display_result = 'none'
        else:
            display_form = 'none'

            if lamda is not None and complexity is not None and gamma is not None and iterasi is not None:
                display_result = 'block'

                data_normalisasi = normalisasi.get_normalisasi(level)['n_data_normalisasi']

                matriks = training.get_matriks(data_normalisasi, lamda, float(s))
                n_data_normalisasi = matriks['n_data_normalisasi']
                n_list_data_kernel = matriks['n_list_data_kernel']
                n_list_data_matriks = matriks['n_list_data_matriks']
                n_list_data_matriks_view = matriks['n_list_data_matriks_view']

                data_iterasi = training.get_iterasi(n_list_data_matriks, complexity, gamma, iterasi)

                if len(data_iterasi) > 0:
                    dt = training.get_bias(level, n_data_normalisasi,
                                           data_iterasi[len(data_iterasi) - 1]['data_alfa_baru'], n_list_data_kernel)
                    data_bobot = dt['data_bobot']
                    bias = dt['bias']
            else:
                display_result = 'none'

        context = {
            'level': level,
            'n_data_normalisasi': n_data_normalisasi,
            'n_list_data_matriks_view': n_list_data_matriks_view,
            'data_iterasi': data_iterasi,
            'data_bobot': data_bobot,
            'bias': bias,
            'display_form': display_form,
            'display_result': display_result,
            'form': form
        }

        return context

    # Handle POST HTTP requests
    def post(self, request, *args, **kwargs):
        form = ParameterForm(request.POST)

        level = self.kwargs['level']

        if form.is_valid():
            lamda = float(form.cleaned_data['lamda'])
            complexity = float(form.cleaned_data['complexity'])
            gamma = float(form.cleaned_data['gamma'])
            iterasi = int(form.cleaned_data['iterasi'])

            try:
                param = Parameter.objects.get(id='1')
                s = param.sigma
                if s is None or not s.strip():
                    s = '2'
            except Parameter.DoesNotExist:
                param = Parameter()
                param.id = '1'
                s = '2'

            param.sigma = s
            param.lamda = lamda
            param.complexity = complexity
            param.gamma = gamma
            param.iterasi = iterasi
            param.save()

            # Save to DB
            normalisasi.save_normalisasi_to_db()

            l_n_data_normalisasi = []
            l_n_list_data_matriks_view = []
            l_data_iterasi = []
            l_data_bobot = []
            l_bias = 0

            for i in range(7):
                lv = i + 1
                data_normalisasi = normalisasi.get_normalisasi(lv)['n_data_normalisasi']

                matriks = training.get_matriks(data_normalisasi, lamda, float(s))
                n_data_normalisasi = matriks['n_data_normalisasi']
                n_list_data_kernel = matriks['n_list_data_kernel']
                n_list_data_matriks = matriks['n_list_data_matriks']
                n_list_data_matriks_view = matriks['n_list_data_matriks_view']

                data_iterasi = training.get_iterasi(n_list_data_matriks, complexity, gamma, iterasi)

                data_bobot = []
                bias = 0
                if len(data_iterasi) > 0:
                    dt = training.get_bias(lv, n_data_normalisasi, data_iterasi[len(data_iterasi) - 1]['data_alfa_baru'], n_list_data_kernel)
                    data_bobot = dt['data_bobot']
                    bias = dt['bias']

                if lv == level:
                    l_n_data_normalisasi = n_data_normalisasi
                    l_n_list_data_matriks_view = n_list_data_matriks_view
                    l_data_iterasi = data_iterasi
                    l_data_bobot = data_bobot
                    l_bias = bias

            context = {
                'level': level,
                'n_data_normalisasi': l_n_data_normalisasi,
                'n_list_data_matriks_view': l_n_list_data_matriks_view,
                'data_iterasi': l_data_iterasi,
                'data_bobot': l_data_bobot,
                'bias': l_bias,
                'display_form': 'block',
                'display_result': 'block',
                'form': form
            }

            return render(request, self.template_name, {self.context_object_name: context})
        else:
            context = {
                'level': level,
                'n_data_normalisasi': [],
                'n_list_data_matriks_view': [],
                'data_iterasi': [],
                'display_form': 'block',
                'display_result': 'none',
                'form': form
            }

            return render(request, self.template_name, {self.context_object_name: context})