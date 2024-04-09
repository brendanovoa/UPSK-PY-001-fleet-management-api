from django.db import models

# Create your models here.

class taxis(models.Model):
    id = models.AutoField(primary_key=True)
    plate = models.CharField(max_length=20)

    class Meta:
        verbose_name_plural = "taxis"

    def __str__(self):
        return self.plate

class trajectories(models.Model):
    id = models.AutoField(primary_key=True)
    taxi_id = models.ForeignKey(taxis, on_delete=models.CASCADE)
    date = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        verbose_name_plural = "trajectories"
    
    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')