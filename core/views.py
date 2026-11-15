import json
from decimal import Decimal, InvalidOperation
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError                    
from django.db import IntegrityError, transaction                    
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_time, parse_datetime, parse_duration
from django.views.decorators.http import require_POST                 
from . import models as m
from .models import Student



def _int(v, default=0):
    return int(v) if v not in (None, "") else default


def _aware(dt):
    if dt and settings.USE_TZ and timezone.is_naive(dt):
        return timezone.make_aware(dt)
    return dt



def _save(obj):
    obj.full_clean()
    obj.save()
    return obj



def _page_context():
    return {
        "status_choices": m.TextDemo.Status.choices,
        "py_files": sorted(str(f) for f in settings.BASE_DIR.glob("*.py")),
        "users": get_user_model().objects.all(),
        "authors": m.LabAuthor.objects.all(),
        "courses": m.LabCourse.objects.all(),

        "text_list": m.TextDemo.objects.all(),
        "number_list": m.NumberDemo.objects.all(),
        "datetime_list": m.DateTimeDemo.objects.all(),
        "file_list": m.FileDemo.objects.all(),
        "misc_list": m.MiscDemo.objects.all(),
        "author_list": m.LabAuthor.objects.all(),
        "book_list": m.LabBook.objects.select_related("author", "editor"),
        "profile_list": m.LabProfile.objects.select_related("user"),
        "course_list": m.LabCourse.objects.all(),
        "student_list": m.LabStudent.objects.prefetch_related("courses"), 
    }



#  STUDENT CRUD

def home(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()                     
        try:                                                             
            roll_no = int(request.POST.get("roll_no", "").strip())      
        except ValueError:                                               
            messages.error(request, "Valid Roll Number likho.")         
            return redirect("home")                                     
        if name:                                                         
            Student.objects.create(name=name, roll_no=roll_no)
            messages.success(request, "Student add ho gaya.")            
        return redirect("home")

    
    context = _page_context()
    context["students"] = Student.objects.all()
    return render(request, "index.html", context)


@require_POST                                                           
def delete(request, id):
    student = get_object_or_404(Student, id=id)                       
    student.delete()
    messages.warning(request, "Student delete ho gaya.")      
    return redirect("home")


def update(request, id):
    student = get_object_or_404(Student, id=id)                          

    if request.method == "POST":
        name = request.POST.get("name", "").strip()                      
        try:                                                             
            roll_no = int(request.POST.get("roll_no", "").strip())       
        except ValueError:                                               
            return render(request, "update.html", {"student": student})  
        if name:                                                         
            student.name = name
            student.roll_no = roll_no
            student.save()
            messages.success(request, "Student update ho gaya.")    
            return redirect("home")

   
    return render(request, "update.html", {"student": student})




def save_text(request):
    p = request.POST
    _save(m.TextDemo(
        char=p.get("char", ""),
        text=p.get("text", ""),
        slug=p.get("slug", ""),
        email=p.get("email", ""),
        url=p.get("url", ""),
        ip=p.get("ip") or None,
        status=p.get("status", "A"),
    ))


def save_number(request):
    p = request.POST
    _save(m.NumberDemo(
        integer=_int(p.get("integer")),
        small=_int(p.get("small")),
        big=_int(p.get("big")),
        pos_int=_int(p.get("pos_int")),
        pos_small=_int(p.get("pos_small")),
        pos_big=_int(p.get("pos_big")),
        float_num=float(p.get("float_num") or 0),
        decimal_num=Decimal(p.get("decimal_num") or ""),
        rating=_int(p.get("rating"), 5),
    ))


def save_datetime(request):
    p = request.POST
    _save(m.DateTimeDemo(
        date=parse_date(p.get("date", "")),
        time=parse_time(p.get("time", "")),
        datetime=_aware(parse_datetime(p.get("datetime", ""))),
        duration=parse_duration(p.get("duration", "")),
    ))


def save_file(request):
    _save(m.FileDemo(
        title=request.POST.get("title", ""),
        file=request.FILES.get("file") or "",
        image=request.FILES.get("image") or None,
        py_file=request.POST.get("py_file", ""),
    ))


def save_misc(request):
    p = request.POST
    verified = {"true": True, "false": False}.get(p.get("is_verified")) 
    _save(m.MiscDemo(
        is_active="is_active" in p,                 
        is_verified=verified,
        data=json.loads(p.get("data") or "{}"),
        price=Decimal(p.get("price") or 0),
        qty=_int(p.get("qty"), 1),
    ))


def save_author(request):
    _save(m.LabAuthor(name=request.POST.get("name", "")))


def save_book(request):
    p = request.POST
    _save(m.LabBook(
        title=p.get("title", ""),
        author_id=p.get("author") or None,
        editor_id=p.get("editor") or None,
    ))


def save_profile(request):
    p = request.POST
    _save(m.LabProfile(user_id=p.get("user") or None, bio=p.get("bio", "")))


def save_course(request):
    _save(m.LabCourse(name=request.POST.get("name", "")))


def save_student(request):
    with transaction.atomic():
        student = _save(m.LabStudent(name=request.POST.get("name", "")))
        student.courses.set(request.POST.getlist("courses"))   

HANDLERS = {
    "text": save_text,
    "number": save_number,
    "datetime": save_datetime,
    "file": save_file,
    "misc": save_misc,
    "author": save_author,
    "book": save_book,
    "profile": save_profile,
    "course": save_course,
    "student": save_student,
}

MODELS = {
    "text": m.TextDemo,
    "number": m.NumberDemo,
    "datetime": m.DateTimeDemo,
    "file": m.FileDemo,
    "misc": m.MiscDemo,
    "author": m.LabAuthor,
    "book": m.LabBook,
    "profile": m.LabProfile,
    "course": m.LabCourse,
    "student": m.LabStudent,
}



def _validation_text(e):
    if hasattr(e, "error_dict"):
        return "; ".join(f"{field}: {' '.join(errs)}" for field, errs in e.message_dict.items())
    return "; ".join(e.messages)


def lab_index(request):
    if request.method == "POST":
        handler = HANDLERS.get(request.POST.get("form_type"))
        if handler is None:
            messages.error(request, "Form type galat hai.")
        else:
            try:
                handler(request)
                messages.success(request, "Save ho gaya!")
            except ValidationError as e:                                         
                messages.error(request, f"Validation error: {_validation_text(e)}")
            except InvalidOperation:                                          
                messages.error(request, "Decimal field mein valid number likho.")
            except (ValueError, TypeError) as e:                                 
                messages.error(request, f"Galat value di gayi hai: {e}")
            except IntegrityError as e:                                          
                messages.error(request, f"Database error: {e}")
    return redirect("home")                                                      


@require_POST                                                                  
def lab_delete(request, key, pk):
    model = MODELS.get(key)
    if model is None:                                                         
        messages.error(request, "Model type galat hai.")
    else:
        get_object_or_404(model, pk=pk).delete()
        messages.warning(request, "Delete ho gaya.")
    return redirect("home")                                               
