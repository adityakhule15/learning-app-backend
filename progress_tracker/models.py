from time import timezone
from django.db import models
from django.contrib.auth import get_user_model
from lessons.models import Lesson

User = get_user_model()


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='progress')
    last_step_completed = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    total_time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    started_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'lesson']
        indexes = [
            models.Index(fields=['user', 'lesson']),
            models.Index(fields=['completed']),
        ]
        ordering = ['-last_updated']
    
    def __str__(self):
        status = "Completed" if self.completed else "In Progress"
        return f"{self.user.phone} - {self.lesson.title} ({status})"
    
    def save(self, *args, **kwargs):
        # Check if lesson is completed
        if not self.completed:
            total_steps = self.lesson.steps.count()
            if self.last_step_completed >= total_steps:
                self.completed = True
                self.completed_at = timezone.now()
        super().save(*args, **kwargs)

        