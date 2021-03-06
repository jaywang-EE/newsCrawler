from django.db import models
from django.core.validators import MinLengthValidator

class News(models.Model):
    title = models.CharField(
            max_length=200, help_text='title url')

    url = models.CharField(
            max_length=200, help_text='news url',
            #validators=[MinLengthValidator(2, "Url must be greater than 1 character")]
    )

    image_url = models.CharField(max_length=200, help_text='image url')

    category = models.CharField(max_length=100, help_text='category')

    author = models.CharField(max_length=40, null=True, help_text='author')
    
    source = models.CharField(max_length=40, null=True, help_text='source')

    date = models.DateField()
    

    def __str__(self):
        return self.title


