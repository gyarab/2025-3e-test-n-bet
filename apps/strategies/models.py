from django.db import models

# Create your models here.

class Strategy(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    base_strategy = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='derived_strategies'
    )
    parameters = models.JSONField(default=dict, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
