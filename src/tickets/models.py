import uuid
import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

def validate_poster_file(file):
    max_size = 5 * 1024 * 1024 # 5 MB
    if file.size > max_size:
        raise ValidationError(f"File size must be under 5MB.")
    
    ext = os.path.splitext(file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png']
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions are: {', '.join(valid_extensions)}")

# 1. Concert Model (For Admin CRUD & User browsing)
class Concert(models.Model):
    # SECURITY: Using UUIDs instead of sequential IDs prevents IDOR attacks (OWASP A5)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    # Secured file upload
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, validators=[validate_poster_file]) 

    @property
    def is_past(self):
        return self.date < timezone.now()

    def __str__(self):
        return self.title

# 2. Booking Model (The secure CRUD booking module)
class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    concert = models.ForeignKey(Concert, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.concert.title}"

# 3. Audit Log Model (Mandatory requirement)
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - {self.action}"