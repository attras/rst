from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,Group,Permission
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid
from django.core.exceptions import ValidationError
import random,string
from django.utils.text import slugify
from taggit.managers import TaggableManager
# Create your models here.

class CreateUpdateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archive_at = models.DateTimeField(default = None, null=True)
    deleted_at = models.DateTimeField(default = None, null=True)
    class Meta:
        abstract = True

class Faq(CreateUpdateTime):
    faq_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    pertanyaan = models.CharField(max_length=225)
    jawaban = models.CharField(max_length=225)

LEVEL_WILAYAH = (
    (1, 'Provinsi'),
    (2, 'Kabupaten'),
    (3, 'Kecamatan'),
    (4, 'Kampung')
)
class Tahun(models.Model):
    tahun = models.IntegerField(default=2024)
    class Meta:
        abstract = True

class MasterWilayah(Tahun, CreateUpdateTime):
    wilayah_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    wilayah_parent = models.ForeignKey('self', default=None, on_delete=models.PROTECT, null=True)
    wilayah_nama = models.TextField()
    wilayah_level = models.CharField(default=None, choices=LEVEL_WILAYAH, max_length=1)
    wilayah_status = models.BooleanField(default=True)