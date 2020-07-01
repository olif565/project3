import math
import numpy as np

from home.models import DataTesting, HasilTraining, Parameter, DataBias, Diagnosis


def proses_testing():

    data_testing = get_data_testing()
    sigma = get_sigma()

    # print(data_testing)

    datalevel = {
        1: 'D1',
        2: 'D2',
        3: 'DT',
        4: 'T3',
        5: 'T2',
        6: 'T1',
        7: 'PD'
    }

    list_data_kernel = []

    for i, x in enumerate(data_testing):

        hasil = ''

        data_kernel = []

        for lvl in range(7):

            level = lvl + 1

            data_training = get_data_training(level)

            db = DataBias.objects.filter(level=str(level))

            bias = 0
            if len(db) > 0:
                bias = float(db[0].bias)

            data_k = []
            data_alpha = []

            for j, y in enumerate(data_training):
                n1 = math.pow((float(y['n_ch4']) - float(x['persen_ch4'])), 2)
                n2 = math.pow((float(y['n_c2h4']) - float(x['persen_c2h4'])), 2)
                n3 = math.pow((float(y['n_c2h2']) - float(x['persen_c2h2'])), 2)

                k = math.exp((-(n1 + n2 + n3)) / (2 * (math.pow(float(sigma), 2))))

                a = float(y['alpha']) * float(y['kelas']) * k

                data_k.append([k, a])

                data_alpha.append(a)

            data_kernel.append(data_k)

            sum_data_alpha = sum(data_alpha)

            f = sum_data_alpha + bias

            fk = np.sign(f)

            # Save klasifikasi to DB
            data_db = Diagnosis.objects.filter(no=str(x['no']))
            if len(data_db) > 0:
                dd = data_db[0]
            else:
                dd = Diagnosis()
                dd.no = str(x['no'])

            if level == 1:
                dd.f1 = f
            if level == 2:
                dd.f2 = f
            if level == 3:
                dd.f3 = f
            if level == 4:
                dd.f4 = f
            if level == 5:
                dd.f5 = f
            if level == 6:
                dd.f6 = f
            if level == 7:
                dd.f7 = f

            aktual = ''
            data_db = DataTesting.objects.filter(no=str(x['no']))
            if len(data_db) > 0:
                aktual = data_db[0].fault

            # print(str(x['no']) + " ~ " + str(level) + " ~ " + str(sum_data_alpha) + " ~ " + str(f))

            if fk == 1:
                hasil = datalevel.get(level)
                h = '1 di level ' + str(level) + ' = ' + hasil

                akurasi = 0
                if hasil == aktual:
                    akurasi = 1

                dd.hasil_code = hasil
                dd.hasil = h
                dd.aktual = aktual
                dd.akurasi = akurasi
                dd.save()
                break

            # elif level == 6 and fk == -1:
            #     hasil = datalevel.get(7)
            #     h = '-1 di level ' + str(level) + ' = ' + hasil
            #
            #     dd.hasil = h
            #     dd.aktual = aktual
            #     dd.akurasi = 0
            #     dd.save()

            else:
                dd.aktual = aktual
                dd.akurasi = 0
                dd.save()

        list_data_kernel.append(
            {
                'no': x['no'],
                'data_kernel': data_kernel
            }
        )

        db = DataTesting.objects.filter(no=str(x['no']))
        if len(db) > 0:
            dt = db[0]
            dt.hasil = hasil
            dt.save()

    return list_data_kernel


def get_data_testing():

    listdata = DataTesting.objects.all()
    list_persen_ch4 = DataTesting.objects.values_list('persen_ch4', flat=True)
    list_persen_c2h4 = DataTesting.objects.values_list('persen_c2h4', flat=True)
    list_persen_c2h2 = DataTesting.objects.values_list('persen_c2h2', flat=True)

    if len(list_persen_ch4) > 0:
        min_persen_ch4 = min([float(i) for i in list_persen_ch4])
        max_persen_ch4 = max([float(i) for i in list_persen_ch4])
    else:
        min_persen_ch4 = 0
        max_persen_ch4 = 0

    if len(list_persen_c2h4) > 0:
        min_persen_c2h4 = min([float(i) for i in list_persen_c2h4])
        max_persen_c2h4 = max([float(i) for i in list_persen_c2h4])
    else:
        min_persen_c2h4 = 0
        max_persen_c2h4 = 0

    if len(list_persen_c2h2) > 0:
        min_persen_c2h2 = min([float(i) for i in list_persen_c2h2])
        max_persen_c2h2 = max([float(i) for i in list_persen_c2h2])
    else:
        min_persen_c2h2 = 0
        max_persen_c2h2 = 0

    minvalue = {
        'persen_ch4': min_persen_ch4,
        'persen_c2h4': min_persen_c2h4,
        'persen_c2h2': min_persen_c2h2
    }

    maxvalue = {
        'persen_ch4': max_persen_ch4,
        'persen_c2h4': max_persen_c2h4,
        'persen_c2h2': max_persen_c2h2
    }

    n_data_normalisasi = []
    n_persen_ch4 = []
    n_persen_c2h4 = []
    n_persen_c2h2 = []

    for x in listdata:
        data = {
            'no': x.no,
            'persen_ch4': 0,
            'persen_c2h4': 0,
            'persen_c2h2': 0
        }
        n_data_normalisasi.append(data)

    for i, x in enumerate(list_persen_ch4):
        minmax = maxvalue['persen_ch4'] - minvalue['persen_ch4']
        if minmax > 0:
            n = (float(x) - minvalue['persen_ch4']) / minmax
            n_persen_ch4.append(n)
            n_data_normalisasi[i]['persen_ch4'] = float(n)

    for i, x in enumerate(list_persen_c2h4):
        minmax = maxvalue['persen_c2h4'] - minvalue['persen_c2h4']
        if minmax > 0:
            n = (float(x) - minvalue['persen_c2h4']) / minmax
            n_persen_c2h4.append(n)
            n_data_normalisasi[i]['persen_c2h4'] = float(n)

    for i, x in enumerate(list_persen_c2h2):
        minmax = maxvalue['persen_c2h2'] - minvalue['persen_c2h2']
        if minmax > 0:
            n = (float(x) - minvalue['persen_c2h2']) / minmax
            n_persen_c2h2.append(n)
            n_data_normalisasi[i]['persen_c2h2'] = float(n)

    return n_data_normalisasi


def get_data_training(level):

    db = HasilTraining.objects.filter(level=level)
    data_training = []

    for x in db:
        data = {
            'no': x.no,
            'level': x.level,
            'n_ch4': x.n_ch4,
            'n_c2h4': x.n_c2h4,
            'n_c2h2': x.n_c2h2,
            'fault': x.fault,
            'kelas': x.kelas,
            'alpha': x.alpha
        }
        data_training.append(data)

    return data_training


def get_sigma():
    db = Parameter.objects.all()

    sigma = 2
    if len(db) > 0:
        sigma = db[0].sigma

    return sigma
