from django.db import models


class ProductQue(models.Model):
    date = models.DateField(unique=True)
    is_resolved = models.BooleanField(default=False)
    status = models.TextField(blank=True, null=True)

    def mark_resolved(self, status):
        self.status = status
        self.is_resolved = True
        self.save()

    def mark_unresolved(self, status):
        self.status = status
        self.save()
