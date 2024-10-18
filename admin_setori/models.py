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

def validate_file_gambar(value):
    dokumen =[
                'image/jpeg',
                'image/png',
                'image/jpg',
            ]
    if value.file.content_type not in dokumen:
        raise ValidationError(u'Pastikan ekstensi file adalah .jpg, .jpeg atau .png.')
    
def validate_file_size_gambar(value):
    filesize= value.size
    
    # if filesize > 5242880:
    if filesize > 2242880:
        raise ValidationError("Pastikan ukuran File dibawah 2 MB.")
    else:
        return value
       
class AccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, phone, password, **extra_fields):
        values = [email, username, phone,]
        field_value_map = dict(zip(self.model.REQUIRED_FIELDS, values))
        for field_name, value in field_value_map.items():
            if not value:
                raise ValueError('The {} value must be set'.format(field_name))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_verified', True)
        return self._create_user(email, username, phone, password, **extra_fields)

    def create_superuser(self, email, username, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_verified') is not True:
            raise ValueError('Superuser must have is_verified=True.')

        return self._create_user(email, username, phone, password, **extra_fields)

ROLE_CHOICES = [
    ('super_admin','Super Admin'),
    ('admin', 'Admin'),
    ('posting', 'Posting'),
    ('data_kesehatan', 'data_kesehatan'),
    ]

"""TABEL AKUN UNTUK SELAIN BAWAANNYA DJANGO YANG DIPAKAI"""
class Account(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True)
    phone = models.CharField(max_length=15)
    date_of_birth = models.DateField(blank=True, null=True)
    #avatar = models.ImageField(blank=True, null=True, upload_to='profile/images/avatar/', validators=[validate_file_gambar, validate_file_size_gambar],)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='posting')
    email_verification_token = models.CharField(max_length=100, default='')
    
    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone', 'role']

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name
  



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

class Tahun(models.Model):
    tahun = models.IntegerField(default=2024)
    class Meta:
        abstract = True

LEVEL_WILAYAH = (
    (1, 'Kabupaten'),
    (2, 'Kecamatan'),
    (3, 'Kampung')
)

class MasterWilayah(Tahun, CreateUpdateTime):
    wilayah_id = models.TextField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    wilayah_parent = models.ForeignKey('self', default=None, on_delete=models.PROTECT, null=True)
    wilayah_nama = models.TextField()
    wilayah_level = models.CharField(default=None, choices=LEVEL_WILAYAH, max_length=1)
    wilayah_status = models.BooleanField(default=True)
   


    def get_level_display(self):
        for key, value in LEVEL_WILAYAH:
            if str(key) == self.wilayah_level:
                return value
        return None

class MasterIdentitass(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    identitas = models.CharField(max_length=100)

class Category(models.Model):
    categori_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Slider(CreateUpdateTime):
    id_slider = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    logo = models.ImageField(upload_to='slider/logo',null=True,validators=[validate_file_gambar, validate_file_size_gambar],blank=True )
    foto = models.ImageField(upload_to='slider/background',null=True,validators=[validate_file_gambar, validate_file_size_gambar],blank=True)
    text = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
