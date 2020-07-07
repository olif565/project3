import numpy as np
import pandas as pd

from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

from home.models import Data


def calculate_svm_seq(lamda, complexity, gamma, iterasi, split):

    data = get_normalisasi()

    x = data['x']
    y = data['y']

    # svclassifier = SVC(kernel='rbf', C=complexity, max_iter=iterasi, gamma=gamma, probability=True, decision_function_shape='ovr', break_ties=True, class_weight='balanced')
    # svclassifier = SVC(kernel='rbf', C=complexity, max_iter=iterasi, gamma=gamma, probability=True, decision_function_shape='ovr', break_ties=True)
    svclassifier = SVC(kernel='rbf', C=complexity, max_iter=iterasi, gamma=gamma, probability=True)

    scores = []
    data_evaluasi = []

    cv = StratifiedKFold(n_splits=split, shuffle=True, random_state=42)

    for train_index, test_index in cv.split(x, y):

        x_train, x_test, y_train, y_test = x[train_index], x[test_index], y[train_index], y[test_index]

        svclassifier.fit(x_train, y_train)

        predictions = svclassifier.predict(x_test)

        classification = classification_report(y_test, predictions, output_dict=True)

        evaluasi = []

        if 'D1' in classification:
            data = {
                'label': 'D1',
                'precision': classification['D1']['precision'],
                'recall': classification['D1']['recall'],
                'f1_score': classification['D1']['f1-score']
            }
            evaluasi.append(data)

        if 'D2' in classification:
            data = {
                'label': 'D2',
                'precision': classification['D2']['precision'],
                'recall': classification['D2']['recall'],
                'f1_score': classification['D2']['f1-score']
            }
            evaluasi.append(data)

        if 'DT' in classification:
            data = {
                'label': 'DT',
                'precision': classification['DT']['precision'],
                'recall': classification['DT']['recall'],
                'f1_score': classification['DT']['f1-score']
            }
            evaluasi.append(data)

        if 'T3' in classification:
            data = {
                'label': 'T3',
                'precision': classification['T3']['precision'],
                'recall': classification['T3']['recall'],
                'f1_score': classification['T3']['f1-score']
            }
            evaluasi.append(data)

        if 'T2' in classification:
            data = {
                'label': 'T2',
                'precision': classification['T2']['precision'],
                'recall': classification['T2']['recall'],
                'f1_score': classification['T2']['f1-score']
            }
            evaluasi.append(data)

        if 'T1' in classification:
            data = {
                'label': 'T1',
                'precision': classification['T1']['precision'],
                'recall': classification['T1']['recall'],
                'f1_score': classification['T1']['f1-score']
            }
            evaluasi.append(data)

        if 'PD' in classification:
            data = {
                'label': 'PD',
                'precision': classification['PD']['precision'],
                'recall': classification['PD']['recall'],
                'f1_score': classification['PD']['f1-score']
            }
            evaluasi.append(data)

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


def get_normalisasi():

    df = pd.DataFrame.from_records(Data.objects.all().values())

    x = df.iloc[:, 2:8]
    y = df['fault']

    scaler = StandardScaler()
    scaler.fit(x)

    x = scaler.transform(x)

    print(x)

    data = {
        'x': x,
        'y': y
    }

    return data

