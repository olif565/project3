from django.shortcuts import render
from django.views.generic import ListView

from home.forms import ParameterFormKfold
from home.models import Parameter
from home.views import diagnosis, testing, svm_seq


class IndexView(ListView):
    template_name = 'home_pengujian_2.html'
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

            data_diagnosis = svm_seq.calculate_svm_seq(lamda, complexity, gamma, iterasi, split)
            scores = data_diagnosis['scores']
            scores_mean = data_diagnosis['scores_mean']
            data_evaluasi = data_diagnosis['data_evaluasi']

            context = {
                'scores': scores,
                'scores_mean': scores_mean,
                'data_evaluasi': data_evaluasi,
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
