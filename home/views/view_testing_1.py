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

            param.sigma = s
            param.lamda = lamda
            param.complexity = complexity
            param.gamma = gamma
            param.iterasi = iterasi
            param.save()

            dt_normalisasi = normalisasi.get_normalisasi(1)
            x = dt_normalisasi['data_normalisasi_x']
            y = dt_normalisasi['data_normalisasi_y']

            xk = np.array(x)
            yk = np.array(y)

            cv = StratifiedKFold(n_splits=split, shuffle=True, random_state=42)

            list_accuracy = []

            for train_index, test_index in cv.split(xk, yk):
                xt = train_index.tolist()
                xtest = test_index.tolist()
                print(xtest)

                for a, b in enumerate(xt):
                    xt[a] = xt[a] + 1

                for a, b in enumerate(xtest):
                    xtest[a] = xtest[a] + 1

                data_bias = []

                for i in range(7):
                    lv = i + 1

                    data_normalisasi = normalisasi.get_normalisasi(lv, xt)['n_data_normalisasi']

                    matriks = training.get_matriks(data_normalisasi, lamda, float(s))
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

                    # data_normalisasi_test = normalisasi.get_normalisasi(lv, xtest)['n_data_normalisasi']

                # print( xk[test_index].tolist())
                data_testing = testing.proses_testing(True, xk[test_index].tolist(), xk[train_index].tolist(), data_bias)

                acc = []
                for i, j in enumerate(data_testing):
                    acc.append(j['data_akurasi'])

                list_accuracy.append(sum(acc) / len(data_testing))

                print(sum(acc) / len(data_testing))

            context = {
                'scores': [],
                'scores_mean': sum(list_accuracy) / len(list_accuracy),
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
