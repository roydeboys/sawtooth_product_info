from django.db import models


class ProductQue(models.Model):
    date = models.DateField(unique=True)
    is_resolved = models.BooleanField(default=False)
    status = models.CharField(max_length=250, blank=True, null=True)

    def mark_resolved(self):
        self.is_resolved = True
        self.save()
