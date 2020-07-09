from home.models import Data, HasilTraining
from django.db.models import Q


def get_normalisasi(level):

    proses = proses_normalisasi(level)

    n_data_normalisasi = proses['n_data_normalisasi']
    data_normalisasi_x = proses['data_normalisasi_x']
    data_normalisasi_y = proses['data_normalisasi_y']

    data_normalisasi = {
        'n_data_normalisasi': n_data_normalisasi,
        'data_normalisasi_x': data_normalisasi_x,
        'data_normalisasi_y': data_normalisasi_y
    }

    return data_normalisasi


def save_normalisasi_to_db():
    # Save to DB
    for i in range(7):
        level = i + 1
        save_to_db(proses_normalisasi(level)['n_data_normalisasi'], level)


def proses_normalisasi(level):
    # D1 kelas 1
    # D2 kelas 2
    # DT kelas 3
    # T3 kelas 4
    # T2 kelas 5
    # T1 kelas 6
    # PD kelas 7

    datalevel = {
        1: Data.objects.all(),
        2: Data.objects.filter(~Q(fault='D1')),
        3: Data.objects.filter(~Q(fault='D1') & ~Q(fault='D2')),
        4: Data.objects.filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT')),
        5: Data.objects.filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3')),
        6: Data.objects.filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2')),
        7: Data.objects.filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2') & ~Q(fault='T1'))
    }

    datalevel_persen_ch4 = {
        1: Data.objects.values_list('persen_ch4', flat=True),
        2: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1')),
        3: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2')),
        4: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT')),
        5: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3')),
        6: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2')),
        7: Data.objects.values_list('persen_ch4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2') & ~Q(fault='T1'))
    }

    datalevel_persen_c2h4 = {
        1: Data.objects.values_list('persen_c2h4', flat=True),
        2: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1')),
        3: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2')),
        4: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT')),
        5: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3')),
        6: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2')),
        7: Data.objects.values_list('persen_c2h4', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2') & ~Q(fault='T1'))
    }

    datalevel_persen_c2h2 = {
        1: Data.objects.values_list('persen_c2h2', flat=True),
        2: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1')),
        3: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2')),
        4: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT')),
        5: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3')),
        6: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2')),
        7: Data.objects.values_list('persen_c2h2', flat=True).filter(~Q(fault='D1') & ~Q(fault='D2') & ~Q(fault='DT') & ~Q(fault='T3') & ~Q(fault='T2') & ~Q(fault='T1'))
    }

    listdata = datalevel.get(level)
    list_persen_ch4 = datalevel_persen_ch4.get(level)
    list_persen_c2h4 = datalevel_persen_c2h4.get(level)
    list_persen_c2h2 = datalevel_persen_c2h2.get(level)

    minvalue = {
        'persen_ch4': min([float(i) for i in list_persen_ch4]),
        'persen_c2h4': min([float(i) for i in list_persen_c2h4]),
        'persen_c2h2': min([float(i) for i in list_persen_c2h2])
    }

    maxvalue = {
        'persen_ch4': max([float(i) for i in list_persen_ch4]),
        'persen_c2h4': max([float(i) for i in list_persen_c2h4]),
        'persen_c2h2': max([float(i) for i in list_persen_c2h2])
    }

    n_data_normalisasi = []
    n_persen_ch4 = []
    n_persen_c2h4 = []
    n_persen_c2h2 = []

    data_normalisasi_x = []
    data_normalisasi_y = []

    # Normalisasi
    for x in listdata:
        data = {
            'no': x.no,
            'persen_ch4': 0,
            'persen_c2h4': 0,
            'persen_c2h2': 0,
            'fault': x.fault,
            'kelas': 1
        }
        n_data_normalisasi.append(data)

    for i, x in enumerate(list_persen_ch4):
        n = (float(x) - minvalue['persen_ch4']) / (maxvalue['persen_ch4'] - minvalue['persen_ch4'])
        n_persen_ch4.append(n)
        n_data_normalisasi[i]['persen_ch4'] = float(n)
        data_normalisasi_x.append([float(n), 0, 0, n_data_normalisasi[i]['fault'], 1, 0])

    for i, x in enumerate(list_persen_c2h4):
        n = (float(x) - minvalue['persen_c2h4']) / (maxvalue['persen_c2h4'] - minvalue['persen_c2h4'])
        n_persen_c2h4.append(n)
        n_data_normalisasi[i]['persen_c2h4'] = float(n)
        data_normalisasi_x[i][1] = float(n)

    for i, x in enumerate(list_persen_c2h2):
        n = (float(x) - minvalue['persen_c2h2']) / (maxvalue['persen_c2h2'] - minvalue['persen_c2h2'])
        n_persen_c2h2.append(n)
        n_data_normalisasi[i]['persen_c2h2'] = float(n)
        data_normalisasi_x[i][2] = float(n)

    for i, x in enumerate(n_data_normalisasi):
        if x['fault'] == 'D1':
            x['fault'] = '1'
        elif x['fault'] == 'D2':
            x['fault'] = '2'
        elif x['fault'] == 'DT':
            x['fault'] = '3'
        elif x['fault'] == 'T3':
            x['fault'] = '4'
        elif x['fault'] == 'T2':
            x['fault'] = '5'
        elif x['fault'] == 'T1':
            x['fault'] = '6'
        else:
            x['fault'] = '7'

        data_normalisasi_y.append(x['fault'])
        data_normalisasi_x[i][3] = x['fault']

    for i, x in enumerate(n_data_normalisasi):
        if x['fault'] == str(level):
            x['kelas'] = '1'
        else:
            x['kelas'] = '-1'

        data_normalisasi_x[i][4] = x['kelas']

    # End Normalisasi

    context = {
        'n_data_normalisasi': n_data_normalisasi,
        'data_normalisasi_x': data_normalisasi_x,
        'data_normalisasi_y': data_normalisasi_y
    }

    return context


def save_to_db(n_data_normalisasi, level):

    for i, x in enumerate(n_data_normalisasi):
        data = HasilTraining.objects.filter(no=str(i + 1), level=str(level))

        if len(data) > 0:
            datatraining = data[0]
        else:
            datatraining = HasilTraining()
            datatraining.no = str(i + 1)
            datatraining.level = str(level)

        datatraining.n_ch4 = x['persen_ch4']
        datatraining.n_c2h4 = x['persen_c2h4']
        datatraining.n_c2h2 = x['persen_c2h2']
        datatraining.fault = x['fault']
        datatraining.kelas = x['kelas']
        datatraining.save()
