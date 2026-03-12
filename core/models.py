from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class PromptRequest(models.Model):

    TASK_CHOICES = [
        ('summarize', 'Summarize'),
        ('rewrite', 'Rewrite'),
        ('explain', 'Explain'),
        ('generate', 'Generate ideas'),
        ('analyze', 'Analyze text'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_type = models.CharField(max_length=20, choices=TASK_CHOICES)
    prompt_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.task_type}"