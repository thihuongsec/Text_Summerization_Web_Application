from django.db import models

# Create your models here.

class Data(models.Model):
    data_input = models.TextField()
    data_output = models.TextField()

    def __str__(self):
        return f"Input: {self.data_input[:50]}... | Output: {self.data_output[:50]}..."
