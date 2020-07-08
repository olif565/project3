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

            for i in range(7):
                lv = i + 1

                dt_normalisasi = normalisasi.get_normalisasi(lv)
                x = dt_normalisasi['data_normalisasi_x']
                y = dt_normalisasi['data_normalisasi_y']

                cv = StratifiedKFold(n_splits=split, shuffle=True, random_state=42)

                for train_index, test_index in cv.split(x, y):
                    


            context = {
                'scores': [],
                'scores_mean': 0,
                'data_evaluasi': [],
                'display': 'none',
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
