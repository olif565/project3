from django.db import models


class Data(models.Model):
    no = models.CharField("No", max_length=50, blank=True, null=True)
    ppm_ch4 = models.CharField("ppm CH4", max_length=50, blank=True, null=True)
    ppm_c2h4 = models.CharField("ppm C2H4", max_length=50, blank=True, null=True)
    ppm_c2h2 = models.CharField("ppm C2H2", max_length=50, blank=True, null=True)
    persen_ch4 = models.CharField("%CH4", max_length=50, blank=True, null=True)
    persen_c2h4 = models.CharField("%C2H4", max_length=50, blank=True, null=True)
    persen_c2h2 = models.CharField("%C2H2", max_length=50, blank=True, null=True)
    fault = models.CharField("Fault", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.no


class HasilTraining(models.Model):
    no = models.CharField("No", max_length=50, blank=True, null=True)
    level = models.CharField("Level", max_length=50, blank=True, null=True)
    n_ch4 = models.CharField("%CH4", max_length=50, blank=True, null=True)
    n_c2h4 = models.CharField("%C2H4", max_length=50, blank=True, null=True)
    n_c2h2 = models.CharField("%C2H2", max_length=50, blank=True, null=True)
    fault = models.CharField("Fault", max_length=50, blank=True, null=True)
    kelas = models.CharField("Kelas", max_length=50, blank=True, null=True)
    alpha = models.CharField("Alpha", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.no


class DataBias(models.Model):
    level = models.CharField("Level", max_length=50, blank=True, null=True)
    bias = models.CharField("Bias", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.level


class DataTesting(models.Model):
    no = models.CharField("No", max_length=50, blank=False, null=True)
    ppm_ch4 = models.CharField("ppm CH4", max_length=50, blank=True, null=True)
    ppm_c2h4 = models.CharField("ppm C2H4", max_length=50, blank=True, null=True)
    ppm_c2h2 = models.CharField("ppm C2H2", max_length=50, blank=True, null=True)
    persen_ch4 = models.CharField("%CH4", max_length=50, blank=False, null=True)
    persen_c2h4 = models.CharField("%C2H4", max_length=50, blank=False, null=True)
    persen_c2h2 = models.CharField("%C2H2", max_length=50, blank=False, null=True)
    fault = models.CharField("Fault", max_length=50, blank=True, null=True)
    hasil = models.CharField("Hasil", max_length=50, blank=True, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.no


class Parameter(models.Model):
    id = models.IntegerField('id', primary_key=True)
    lamda = models.CharField('Lambda', max_length=100, blank=True, null=True)
    sigma = models.CharField('Sigma', max_length=100, blank=True, null=True)
    complexity = models.CharField('Complexity', max_length=100, blank=True, null=True)
    gamma = models.CharField('Gamma', max_length=100, blank=True, null=True)
    iterasi = models.CharField('Iterasi', max_length=100, blank=True, null=True)

    def __str__(self):
        return self.id


class Diagnosis(models.Model):
    no = models.CharField("No", max_length=50, blank=False, null=True)
    f1 = models.CharField("f1", max_length=50, blank=False, null=True)
    f2 = models.CharField("f2", max_length=50, blank=False, null=True)
    f3 = models.CharField("f3", max_length=50, blank=False, null=True)
    f4 = models.CharField("f4", max_length=50, blank=False, null=True)
    f5 = models.CharField("f5", max_length=50, blank=False, null=True)
    f6 = models.CharField("f6", max_length=50, blank=False, null=True)
    f7 = models.CharField("f7", max_length=50, blank=False, null=True)
    hasil_code = models.CharField("Hasil", max_length=50, blank=True, null=True)
    hasil = models.CharField("Hasil", max_length=50, blank=True, null=True)
    aktual = models.CharField("Aktual", max_length=50, blank=False, null=True)
    akurasi = models.CharField("Akurasi", max_length=50, blank=False, null=True)
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.no


class FaultDesc(models.Model):
    code = models.CharField("Kode", max_length=50, blank=False, null=True)
    desc = models.CharField("Keterangan", max_length=300, blank=False, null=True)

    def __str__(self):
        return self.code
