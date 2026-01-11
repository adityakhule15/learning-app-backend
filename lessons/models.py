from django.db import models


class Lesson(models.Model):
    CATEGORY_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('upi', 'UPI'),
        ('basic', 'Basic'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
        ('mr', 'Marathi'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
    order = models.IntegerField(default=0)
    thumbnail_url = models.URLField(blank=True)
    estimated_duration = models.IntegerField(help_text="Duration in minutes", default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['category', 'language']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_language_display()})"


class LessonStep(models.Model):
    STEP_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Video'),
        ('simulation', 'Simulation'),
        ('quiz', 'Quiz'),
    ]
    
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='steps')
    step_number = models.IntegerField()
    title = models.CharField(max_length=255)
    instruction_text = models.TextField()
    step_type = models.CharField(max_length=20, choices=STEP_TYPE_CHOICES, default='text')
    media_url = models.URLField(blank=True, null=True)
    media_caption = models.CharField(max_length=255, blank=True)
    estimated_duration = models.IntegerField(help_text="Duration in seconds", default=30)
    is_interactive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['lesson', 'step_number']
        unique_together = ['lesson', 'step_number']
    
    def __str__(self):
        return f"Step {self.step_number}: {self.title}"
    
    