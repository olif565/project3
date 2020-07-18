import numpy as np

from django.shortcuts import render
from django.views.generic import ListView
from sklearn.model_selection import StratifiedKFold

from home.forms import ParameterFormKfold
from home.models import Parameter
from home.views import diagnosis, testing, svm_seq, training, normalisasi


class IndexView(ListView):
    template_name = 'home_pengujian_1.html'
    context_object_name = 'data'

    def get_queryset(self, **kwargs):

        try:
            data = Parameter.objects.get(id='1')
            if data is None:
                form = ParameterFormKfold()
            else:
                form = ParameterFormKfold(initial={
                    'sigma': data.sigma,
                    'lamda': data.lamda,
                    'complexity': data.complexity,
                    'gamma': data.gamma,
                    'iterasi': data.iterasi,
                    'split': '5'
                })
        except Parameter.DoesNotExist:
            form = ParameterFormKfold()

        context = {
            'scores': [],
            'scores_mean': 0,
            'data_evaluasi': [],
            'display': 'none',
            'form': form
        }

        return context

    # Handle POST HTTP requests
    def post(self, request, *args, **kwargs):
        form = ParameterFormKfold(request.POST)

        if form.is_valid():
            sigma = float(form.cleaned_data['sigma'])
            lamda = float(form.cleaned_data['lamda'])
            complexity = float(form.cleaned_data['complexity'])
            gamma = float(form.cleaned_data['gamma'])
            iterasi = int(form.cleaned_data['iterasi'])
            split = int(form.cleaned_data['split'])

            try:
                param = Parameter.objects.get(id='1')
                s = param.sigma
                if s is None or not s.strip():
                    s = '2'
            except Parameter.DoesNotExist:
                param = Parameter()
                param.id = '1'
                s = '2'

            param.sigma = sigma
            param.lamda = lamda
            param.complexity = complexity
            param.gamma = gamma
            param.iterasi = iterasi
            param.save()

            list_data_bias = []

            cv = StratifiedKFold(n_splits=split, shuffle=True, random_state=42)

            for i in range(7):
                lv = i + 1

                dt_normalisasi = normalisasi.get_normalisasi(lv)
                x = dt_normalisasi['data_normalisasi_x']
                y = dt_normalisasi['data_normalisasi_y']

                xK = np.array(x)
                yK = np.array(y)

                data_bias = []

                for train_index, test_index in cv.split(xK, yK):

                    matriks = training.get_matriks(xK[train_index].tolist(), lamda, float(s), True)
                    n_data_normalisasi = matriks['n_data_normalisasi']
                    n_list_data_kernel = matriks['n_list_data_kernel']
                    n_list_data_matriks = matriks['n_list_data_matriks']

                    data_iterasi = training.get_iterasi(n_list_data_matriks, complexity, gamma, iterasi)
                    data_alpha = data_iterasi[len(data_iterasi) - 1]['data_alfa_baru']

                    for j, x in enumerate(n_data_normalisasi):
                        x[5] = data_alpha[j]

                    bias = 0
                    if len(data_iterasi) > 0:
                        dt = training.get_bias(lv, n_data_normalisasi, data_alpha, n_list_data_kernel, False)
                        bias = dt['bias']

                    data_bias.append(bias)

                list_data_bias.append(data_bias)

            accuracy = []

            for i in range(7):
                lv = i + 1

                dt_normalisasi = normalisasi.get_normalisasi(lv)
                x = dt_normalisasi['data_normalisasi_x']
                y = dt_normalisasi['data_normalisasi_y']

                xK = np.array(x)
                yK = np.array(y)

                data_akurasi = []

                y = 0

                for train_index, test_index in cv.split(xK, yK):

                    y = y + 1

                    matriks = training.get_matriks(xK[train_index].tolist(), lamda, float(s), True)
                    n_data_normalisasi = matriks['n_data_normalisasi']
                    n_list_data_matriks = matriks['n_list_data_matriks']

                    data_iterasi = training.get_iterasi(n_list_data_matriks, complexity, gamma, iterasi)
                    data_alpha = data_iterasi[len(data_iterasi) - 1]['data_alfa_baru']

                    for j, x in enumerate(n_data_normalisasi):
                        x[5] = data_alpha[j]

                    data_testing = testing.proses_testing(True, xK[test_index].tolist(), n_data_normalisasi, list_data_bias[i][y-1])

                    akurasi = []
                    for j, x in enumerate(data_testing):
                        akurasi.append(float(x['data_akurasi']))

                    data_akurasi.append(sum(akurasi) / len(akurasi))

                ac = sum(data_akurasi) / y
                accuracy.append(ac)

            context = {
                'scores': [],
                'scores_mean': (sum(accuracy) / len(accuracy)),
                'data_evaluasi': [],
                'display': 'block',
                'form': form
            }

            return render(request, self.template_name, {self.context_object_name: context})
        else:
            context = {
                'scores': [],
                'scores_mean': 0,
                'data_evaluasi': [],
                'display': 'none',
                'form': form
            }

            return render(request, self.template_name, {self.context_object_name: context})
