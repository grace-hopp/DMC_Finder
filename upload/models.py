from django.db import models
from datetime import datetime
import django
from django.db.models.fields.files import ImageField
from ckeditor.widgets import CKEditorWidget
from django.contrib.sites.models import Site
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

from django.db import models
from image_cropping import ImageRatioField

class Color(models.Model):
    hex_code = models.CharField(max_length=6)
    rgb_red = models.CharField(max_length=3)
    rgb_green = models.CharField(max_length=3)
    rgb_blue = models.CharField(max_length=3)
    dmc_code = models.CharField(max_length=6)
    dmc_name = models.TextField()

class ImageTemp(models.Model):
    img = models.ImageField(upload_to='images', blank=True)