from django.db import models

# Create your models here.
class Movie(models.Model):
  
    class Meta:
        app_label = 'review'
    auto_increment_id = models.AutoField(primary_key=True)    
    movie_title=models.CharField(max_length=20)
    synopsis=models.CharField(max_length=500)
    poster_link=models.CharField(max_length=1000)