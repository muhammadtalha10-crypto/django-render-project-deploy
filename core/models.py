
from django.db import models
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F


class Student(models.Model):
    name = models.CharField(max_length=100 ,null=True,blank=True)
    roll_no = models.IntegerField()



def project_dir():
    return str(settings.BASE_DIR)



class TextDemo(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "A", "Active"
        GRADUATED = "G", "Graduated"
        LEFT = "L", "Left"

    char = models.CharField("Naam (CharField)", max_length=100, help_text="Chhota text")
    text = models.TextField("Description (TextField)", blank=True)
    slug = models.SlugField("Slug (SlugField)", unique=True)
    email = models.EmailField("Email (EmailField)", unique=True)
    url = models.URLField("Website (URLField)", blank=True)
    ip = models.GenericIPAddressField("IP (GenericIPAddressField)", null=True, blank=True)
    status = models.CharField(max_length=1, choices=Status.choices, default=Status.ACTIVE)
    uid = models.UUIDField("UUID", default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.char


class NumberDemo(models.Model):
    integer = models.IntegerField("IntegerField", default=0)
    small = models.SmallIntegerField("SmallIntegerField", default=0)
    big = models.BigIntegerField("BigIntegerField", default=0)
    pos_int = models.PositiveIntegerField("PositiveIntegerField", default=0)
    pos_small = models.PositiveSmallIntegerField("PositiveSmallIntegerField", default=0)
    pos_big = models.PositiveBigIntegerField("PositiveBigIntegerField", default=0)
    float_num = models.FloatField("FloatField", default=0.0)
    decimal_num = models.DecimalField("DecimalField (price)", max_digits=8, decimal_places=2)
    rating = models.PositiveSmallIntegerField(
        "Rating (validators)", default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="1 se 10",
    )

    def __str__(self):
        return f"NumberDemo #{self.pk}"


class DateTimeDemo(models.Model):
    date = models.DateField("DateField")
    time = models.TimeField("TimeField")
    datetime = models.DateTimeField("DateTimeField")
    duration = models.DurationField("DurationField", help_text="Format: 1 02:30:00")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"DateTimeDemo #{self.pk}"


class FileDemo(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField("FileField", upload_to="files/", blank=True)
    image = models.ImageField("ImageField", upload_to="images/%Y/%m/", blank=True, null=True)
    py_file = models.FilePathField("FilePathField", path=project_dir, match=r".*\.py$", blank=True)

    def __str__(self):
        return self.title


class MiscDemo(models.Model):
    is_active = models.BooleanField("BooleanField", default=True)
    is_verified = models.BooleanField("BooleanField (null=True)", null=True, blank=True)
    data = models.JSONField("JSONField", default=dict, blank=True)
    raw = models.BinaryField("BinaryField", editable=False, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    qty = models.PositiveIntegerField(default=1)
    total = models.GeneratedField(
        expression=F("price") * F("qty"),
        output_field=models.DecimalField(max_digits=12, decimal_places=2),
        db_persist=True,
    )

    def __str__(self):
        return f"MiscDemo #{self.pk}"



class LabAuthor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LabBook(models.Model):
    title = models.CharField(max_length=150)
    author = models.ForeignKey(LabAuthor, on_delete=models.CASCADE, related_name="lab_books")
    editor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="lab_edited_books",
    )

    def __str__(self):
        return self.title


class LabProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lab_profile")
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"LabProfile of {self.user}"


class LabCourse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class LabStudent(models.Model):
    name = models.CharField(max_length=100)
    courses = models.ManyToManyField(LabCourse, blank=True, related_name="lab_students")

    def __str__(self):
        return self.name



