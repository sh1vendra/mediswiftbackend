from django.db import models

class Query(models.Model):
    query_text = models.TextField()
    response_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not Query.objects.filter(query_text=self.query_text).exists():
            super().save(*args, **kwargs)

    def __str__(self):
        return self.query_text

class Treatment(models.Model):
    patient_name = models.CharField(max_length=200)
    date_of_illness = models.DateField()
    symptoms = models.TextField()
    disease = models.CharField(max_length=200)  # Added max_length
    diagnosis = models.TextField()
    medication = models.TextField()
    frequency = models.CharField(max_length=100)  # Added max_length
    length_of_treatment = models.CharField(max_length=100)  # Added max_length
    status = models.CharField(max_length=100, default='Pending')  # Added max_length and default

    def __str__(self):
        return f"{self.patient_name} - {self.disease}"
