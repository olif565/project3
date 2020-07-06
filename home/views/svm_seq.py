import numpy as np
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

from home.models import Data
from home.views import normalisasi


def calculate_svm_seq(tahun, const, max_iterasi, gamma, split):

    data = get_normalisasi(tahun)

    x = data['x']
    y = data['y']

    svclassifier = SVC(kernel='rbf', C=const, max_iter=max_iterasi, gamma=gamma, probability=True)

    scores = []              # Menyimpan hasil akurasi masing-masing iterasi
    data_evaluasi = []       # Menyimpan data evaluasi masing-masing iterasi

    # Memanggil fungsi stratifiedKfold dengan parameter input nilai K
    cv = StratifiedKFold(n_splits=split, shuffle=True, random_state=42)

    # Iterasi / pembagian data
    # Membuat indeks untuk membagi data menjadi data training dan testing
    for train_index, test_index in cv.split(x, y):

        # mendeklarasikan data training dan testing dari pembagian data 
        x_train, x_test, y_train, y_test = x[train_index], x[test_index], y[train_index], y[test_index]

        # Membuat model svm dengan 
        # data x (parameter) data training dan y (label) data training
        # Proses training
        svclassifier.fit(x_train, y_train)

        # hasil prediksi data testing
        predictions = svclassifier.predict(x_test)

        # Untuk mendapatkan evaluasi dari klasifikasi
        # Dengan parameter : label testing, hasil prediksi, output_dict 
        classification = classification_report(y_test, predictions, output_dict=True)

        # Hasil evaluasi masing-masing label
        # Dengan evaluasi precision, recall, dan f1 score
        evaluasi = []

        if '1' in classification:
            data1 = {
                'label': 'Berkembang',
                'precision': classification['1']['precision'],
                'recall': classification['1']['recall'],
                'f1_score': classification['1']['f1-score']
            }
            evaluasi.append(data1)

        if '-1' in classification:
            data2 = {
                'label': 'Belum Berkembang',
                'precision': classification['-1']['precision'],
                'recall': classification['-1']['recall'],
                'f1_score': classification['-1']['f1-score']
            }
            evaluasi.append(data2)

        data_evaluasi.append({
            'evaluasi': evaluasi,
            'accuracy': classification['accuracy']
        })

        scores.append(svclassifier.score(x_test, y_test))

    data_svm = {
        'scores': scores,
        'scores_mean': np.mean(scores),
        'data_evaluasi': data_evaluasi
    }

    return data_svm


def get_normalisasi(tahun):

    df = pd.DataFrame.from_records(Data.objects.filter(tahun_smstr=tahun).values())

    # Untuk merubah label kelas menjadi angka 1 dan -1
    df['label_kelas'] = df['label_kelas'].apply(lambda l: 1 if l == 'Berkembang' else -1)

    # Mengambil data dari urutan ke 5 sampai ke 10 
    # variabel x merupakan parameter data, mengambil parameter data  
    # x = df.iloc[:, 5:10]

    # variabel y merupakan label kelas yang sudah dirubah menjadi angka
    y = df['label_kelas']

    # Normalisasi
    x = normalisasi.get_normalisasi(tahun)['data_normalisasi']

    # Proses preprocessing

    # variabel proses dari StandarScaler
    # scaler = StandardScaler()

    # menghitung nilai rataan dan standar deviasi dari data variabel x 
    # untuk NANTI-nya digunakan saat proses scaling. 
    # scaler.fit(x)

    # hasil perhitungan rataan dan standar deviasi sebelumnya (dari ‘fit’) untuk diterapkan ke data
    # x = scaler.transform(x)

    # Membuat array untuk menyimpan variabel data x dan y 
    data = {
        'x': x,
        'y': y
    }

    return data

