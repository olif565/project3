from django.views.generic import ListView

from home.views import diagnosis, testing


class IndexView(ListView):
    template_name = 'home_diagnosis.html'
    context_object_name = 'data_list'

    def get_queryset(self):

        data_diagnosis = diagnosis.get_diagnosis()
        data = data_diagnosis['data']
        akurasi = data_diagnosis['akurasi']

        context = {
            'data': data,
            'akurasi': akurasi
        }

        return context


class NormalisasiView(ListView):
    template_name = 'home_diagnosis_normalisasi.html'
    context_object_name = 'data'

    def get_queryset(self):
        # data_normalisasi = []
        #
        # for x in range(7):
        #     lv = x + 1
        #     data_n = testing.get_data_training(lv)
        #     data_normalisasi.append(data_n)

        data_normalisasi = testing.get_data_testing()

        context = {
            'data_normalisasi': data_normalisasi
        }

        return context


class KernelView(ListView):
    template_name = 'home_diagnosis_kernel.html'
    context_object_name = 'data'

    def get_queryset(self):

        data_kernel = testing.proses_testing()

        context = {
            'data_kernel': data_kernel
        }

        return context
