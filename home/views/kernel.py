import math


def get_kernel(data_normalisasi, sigma):

    n_data_normalisasi = data_normalisasi
    n_list_data_kernel_view = []
    n_list_data_kernel = []

    s = sigma

    for i, x in enumerate(n_data_normalisasi):
        n_data_kernel_view = []
        n_data_kernel = []

        for j, y in enumerate(n_data_normalisasi):
            n1 = math.pow((x['persen_ch4'] - y['persen_ch4']), 2)
            n2 = math.pow((x['persen_c2h4'] - y['persen_c2h4']), 2)
            n3 = math.pow((x['persen_c2h2'] - y['persen_c2h2']), 2)

            k = math.exp((-(n1 + n2 + n3)) / (2 * (math.pow(s, 2))))

            if j == 0:
                # n_data_kernel_view.append(x['no'])
                n_data_kernel_view.append(i+1)

            n_data_kernel_view.append(k)
            n_data_kernel.append(k)

        n_list_data_kernel_view.append(n_data_kernel_view)
        n_list_data_kernel.append(n_data_kernel)

    data_kernel = {
        'n_data_normalisasi': n_data_normalisasi,
        'n_list_data_kernel': n_list_data_kernel,
        'n_list_data_kernel_view': n_list_data_kernel_view
    }

    return data_kernel
