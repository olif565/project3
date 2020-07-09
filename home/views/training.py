import logging
import math

from home.models import DataBias, HasilTraining
from home.views import kernel

from sklearn.model_selection import StratifiedKFold

logger = logging.getLogger(__name__)


def get_matriks(data_normalisasi, lamda, sigma, iskfold=False):

    s = sigma

    datakernel = kernel.get_kernel(data_normalisasi, s, iskfold)
    n_data_normalisasi = datakernel['n_data_normalisasi']
    n_list_data_kernel = datakernel['n_list_data_kernel']
    n_list_data_kernel_view = datakernel['n_list_data_kernel_view']

    n_list_data_matriks = []
    n_list_data_matriks_view = []

    # lambda
    l = lamda

    for i, x in enumerate(n_list_data_kernel):
        n_data_matriks = []
        n_data_matriks_view = []

        if iskfold:
            y_i = int(n_data_normalisasi[i][4])
        else:
            y_i = int(n_data_normalisasi[i]['kelas'])

        for j, y in enumerate(x):
            y = float(n_list_data_kernel[i][j])

            if iskfold:
                y_j = int(n_data_normalisasi[j][4])
            else:
                y_j = int(n_data_normalisasi[j]['kelas'])

            # matrik
            d_ij = y_i * y_j * (y + (math.pow(l, 2)))

            if j == 0:
                # n_data_matriks_view.append(n_data_normalisasi[i]['no'])
                n_data_matriks_view.append(i+1)

            n_data_matriks_view.append(d_ij)
            n_data_matriks.append(d_ij)

        n_list_data_matriks.append(n_data_matriks)
        n_list_data_matriks_view.append(n_data_matriks_view)

    data_kernel = {
        'n_data_normalisasi': n_data_normalisasi,
        'n_list_data_kernel': n_list_data_kernel,
        'n_list_data_matriks': n_list_data_matriks,
        'n_list_data_matriks_view': n_list_data_matriks_view
    }

    return data_kernel


def get_iterasi(list_data_matriks, complexity, gamma, i):

    data_iterasi = []

    alfa_baru = []

    for x in range(i):

        # alpha
        a = 0

        if x == 0:
            a = 0
        else:
            a = alfa_baru

        data_error_rate = get_error_rate(a, list_data_matriks)
        data_delta_alfa = get_delta_alfa(a, data_error_rate, complexity, gamma)
        data_alfa_baru = get_alfa_baru(a, data_delta_alfa)

        alfa_baru = data_alfa_baru

        iterasi = {
            'data_error_rate': data_error_rate,
            'data_delta_alfa': data_delta_alfa,
            'data_alfa_baru': data_alfa_baru
        }

        data_iterasi.append(iterasi)

    return data_iterasi


def get_error_rate(alpha, list_data_matriks):

    data_error_rate = []

    for i, x in enumerate(list_data_matriks):

        for j, y in enumerate(x):

            a = 0
            if alpha == 0:
                a = 0
            else:
                a = alpha[i]

            er = a * float(y)

            if i == 0:
                data_error_rate.append(er)
            else:
                data_error_rate[j] = data_error_rate[j] + er

    return data_error_rate


def get_delta_alfa(alpha, data_error_rate, complexity, gamma):

    # complexity
    comp = complexity

    # gamma
    g = gamma

    data_delta_alfa = []

    for i, x in enumerate(data_error_rate):

        a = 0
        if alpha == 0:
            a = 0
        else:
            a = alpha[i]

        da = min(max(g * (1 - x), -a), (comp - a))
        data_delta_alfa.append(da)

    return data_delta_alfa


def get_alfa_baru(alpha, data_delta_alfa):

    data_alfa_baru = []

    for i, x in enumerate(data_delta_alfa):

        a = 0
        if alpha == 0:
            a = 0
        else:
            a = alpha[i]

        ab = a + x
        data_alfa_baru.append(ab)

    return data_alfa_baru


def get_bias(level, data_normalisasi, data_alpha, data_kernel, iskfold=True):

    alpha1 = []
    alpha2 = []

    for i, x in enumerate(data_alpha):

        if iskfold:
            dn = data_normalisasi[i]['kelas']
        else:
            dn = data_normalisasi[i][4]

        if dn == '1':
            alpha1.append(x)
        else:
            alpha2.append(x)

    kernel = []

    if len(alpha1) > 0:
        index1 = data_alpha.index(max(alpha1))
        kernel.append(data_kernel[index1])

    if len(alpha2) > 0:
        index2 = data_alpha.index(max(alpha2))
        kernel.append(data_kernel[index2])

    # print(level, kernel)

    data_bobot = []
    sum_w = []

    for i, x in enumerate(kernel):

        bobot = []

        if i == 0:
            bobot.append('𝒘.𝒙+')
        if i == 1:
            bobot.append('𝒘.𝒙-')

        for j, y in enumerate(x):

            if iskfold:
                dn = data_normalisasi[j]['kelas']
            else:
                dn = data_normalisasi[j][4]

            w = int(dn) * data_alpha[j] * kernel[i][j]
            bobot.append(w)

            # print(j, data_alpha[j], kernel[i][j])

        data_bobot.append(bobot)

        # print(sum(bobot[1:]))

        sw = sum(bobot[1:])
        sum_w.append(sw)

    bias = -(sum(sum_w)) / 2

    if iskfold:
        # Save Alpha to DB
        for y, x in enumerate(data_alpha):
            db = HasilTraining.objects.filter(no=str(y + 1), level=str(level))

            if len(db) > 0:
                datatraining = db[0]
                datatraining.alpha = x
                datatraining.save()

        # Save Bias to DB
        db = DataBias.objects.filter(level=str(level))

        if len(db) > 0:
            databias = db[0]
        else:
            databias = DataBias()
            databias.level = str(level)

        databias.bias = bias
        databias.save()

    data = {
        'data_bobot': data_bobot,
        'bias': bias
    }

    return data
