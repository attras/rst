from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin,Group,Permission
from django.utils import timezone
from django.core.validators import FileExtensionValidator
import uuid
from django.core.exceptions import ValidationError
import random,string
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.db.models import Sum, Q
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
    pertanyaan = models.TextField()
    jawaban = models.TextField()

class Tahun(models.Model):
    tahun = models.IntegerField(default=2024)
    class Meta:
        abstract = True

LEVEL_WILAYAH = (
    (1, 'Provinsi'),
    (2, 'Kabupaten'),
    (3, 'Kecamatan/distrik'),
    (4, 'Kampung')

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

class Category(CreateUpdateTime):
    categori_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Slider(CreateUpdateTime):
    id_slider = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    logo = models.ImageField(upload_to='slider/logo',null=True,validators=[validate_file_gambar, validate_file_size_gambar],blank=True,default='admin_setori/static/default/defaultlogo.jpeg' )
    foto = models.ImageField(upload_to='slider/background',null=True,validators=[validate_file_gambar, validate_file_size_gambar])
    text = models.CharField(max_length=255)
    status = models.BooleanField(default=False)

class Layanan(CreateUpdateTime):
    id_layanan = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    surat = models.CharField(max_length=100, unique=True)
    syarat = models.TextField()



class News(CreateUpdateTime):
	title = models.CharField(max_length=255)
	thumbnail = models.ImageField(upload_to='artikel', validators=[validate_file_gambar, validate_file_size_gambar], default='artikel/defaultartikel.jpeg')
	content = models.TextField()
	slug = models.SlugField(unique=True, max_length=300)
	category = models.ForeignKey(Category, on_delete=models.RESTRICT)
	created_by = models.ForeignKey(Account, on_delete=models.RESTRICT)
	last_updated_by = models.CharField(max_length=5, null=True, blank=True)
	seen = models.SmallIntegerField(default=0)
	jenis = models.CharField(max_length=255, null=True)

def save(self, *args, **kwargs):
        # Automatically generate slug if not provided
        if not self.slug:
            self.slug = generate_unique_slug(self)
        super(News, self).save(*args, **kwargs)    
  
def generate_unique_slug(instance, new_slug=None, counter=0):
    """
    Generate a unique slug for a News instance based on its title.
    If a slug already exists, append a counter to ensure uniqueness.
    """
    # Initial slug, either passed or generated from the title
    slug = new_slug or slugify(instance.title)
    
    if counter > 0:
        slug = f"{slug}-{counter}"  # Append the counter to the slug if it's not the first attempt

    # Check if the slug already exists
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()

    if qs_exists:
        # Increment counter and recursively call the function until a unique slug is found
        return generate_unique_slug(instance, new_slug=new_slug, counter=counter + 1)
    
    return slug

IDENTITAS_CHOICE = (
    (1, 'OAP'),
    (2, 'Non-OAP')
)

class Data_peduduk(CreateUpdateTime):
    data_penduduk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identitas = models.CharField(max_length=1, choices=IDENTITAS_CHOICE, default=None )
    pria = models.IntegerField(default=0)
    wanita = models.IntegerField(default=0)
    jumlah_kk = models.IntegerField(default=0)
    jumlah_penduduk = models.IntegerField(default=0, null=True)
    wilayah = models.ForeignKey(MasterWilayah, on_delete=models.CASCADE)
    
    def get_identitas_display(self):
        for key, value in IDENTITAS_CHOICE:
            if str(key) == self.identitas:
                return value
        return None
    
   


class Info_wilayah(CreateUpdateTime):
    info_wilayah_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    visi = models.TextField(help_text="Visi kelurahan")
    misi = models.TextField(help_text="Misi kelurahan")
    nama_info_wilayah = models.CharField(max_length=255, help_text="Nama Kelurahan")
    kode_info_wilayah = models.CharField(max_length=50, unique=True, help_text="Kode unik untuk Kelurahan")
    tahun_pembentukan = models.IntegerField(help_text="Tahun pembentukan kelurahan")
    dasar_hukum_pembentukan = models.TextField(help_text="Dasar hukum pembentukan kelurahan")
    kode_pos = models.CharField(max_length=10, help_text="Kode pos kelurahan")
    wilayah = models.ForeignKey(MasterWilayah, on_delete=models.CASCADE)

class Tentang(CreateUpdateTime):
    id_tentang = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False, unique=True)
    gambar = models.ImageField(upload_to='tentang')
    nama_tokoh = models.CharField(max_length=255)
    deskripsi_tokoh = models.TextField()

class Kontak(CreateUpdateTime):
    maps = models.TextField(blank=True, null=True)
    link_ig = models.URLField(blank=True, null=True)
    link_twitter = models.URLField(blank=True, null=True)
    link_facebook = models.URLField(blank=True, null=True)
    alamat = models.TextField(blank=True, null=True)
    email_pengaduan = models.EmailField(blank=True, null=True)
    email_cs = models.EmailField(blank=True, null=True)
    no_pengaduan = models.CharField(max_length=15, blank=True, null=True)
    nama_instansi = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
