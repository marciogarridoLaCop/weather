from django.db import models

class dados(models.Model):    
    Data = models.IntegerField()
    Doy = models.IntegerField()
    Tx = models.FloatField()
    Tn = models.FloatField()
    Rs = models.FloatField()
    U2 = models.FloatField()
    URx = models.FloatField()
    URn = models.FloatField()
    PCP = models.IntegerField()