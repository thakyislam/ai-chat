from django.db import models
from django.contrib.auth.models import User


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

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} | {self.task_type}"


class PromptResponse(models.Model):
    request = models.OneToOneField(PromptRequest, on_delete=models.CASCADE, related_name='response')
    model_name = models.CharField(max_length=100, default='gemini-2.0-flash')
    response_text = models.TextField()
    token_usage = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response to: {self.request}"