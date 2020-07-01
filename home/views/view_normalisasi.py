import logging

from django.views.generic import ListView

from home.views import normalisasi

logger = logging.getLogger(__name__)


class IndexView(ListView):
    template_name = 'home_normalisasi.html'
    context_object_name = 'data'

    def get_queryset(self, **kwargs):

        level = self.kwargs['level']

        display_result = 'block'
        n_data_normalisasi = normalisasi.get_normalisasi(level)['n_data_normalisasi']

        context = {
            'level': level,
            'n_data_normalisasi': n_data_normalisasi,
            'display_result': display_result,
        }

        return context
