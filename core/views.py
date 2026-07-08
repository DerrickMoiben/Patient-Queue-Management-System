from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, PatientRegistrationForm, VisitForm, TriageForm, DoctorConsultationForm
from .models import Patient, Visit


# Create your views here.
def home(request):
    return render(request, 'home.html')







def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "User account created successfully.")
            return redirect("login")
    else:
        form = UserRegistrationForm()

    context = {
        "form": form
    }

    return render(request, "register.html", context)





def login_user(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.role == "receptionist":
                return redirect("reception_dashboard")

            elif user.role == "doctor":
                return redirect("doctor_dashboard")

        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

from django.contrib.auth.decorators import login_required


@login_required
def reception_dashboard(request):
    return render(request, "reception_dashboard.html")


@login_required
def doctor_dashboard(request):
    doctor_visits = Visit.objects.filter(current_department="doctor", status="waiting")
    return render(request, "doctor_dashboard.html", {"doctor_visits": doctor_visits})


def register_patient(request):
    if request.method == "POST":
        # Handle patient registration logic here
        pass
    return render(request, "register_patient.html")



def register_patient(request):
    if request.method == "POST":
       
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient registered successfully.")
            return redirect("reception_dashboard")
    else:
        form = PatientRegistrationForm()
        messages.error(request, "Please correct the errors below.")
        
    return render(request, "register_patient.html", {"form": form})
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Patient, Visit


def start_visit(request):
    patient = None

    if request.method == "POST":
        print(request.POST)

        # Search Patient
        if "search_patient" in request.POST:

            hospital_id = request.POST.get("hospital_id")
            print("Hospital ID:", hospital_id)

            
            patient = Patient.objects.filter(
                hospital_id__iexact=hospital_id.strip()
            ).first()

            if not patient:
                messages.error(request, "Patient not found.")

        # Start Visit
        elif "start_visit" in request.POST:

            patient_id = request.POST.get("patient_id")

            patient = Patient.objects.get(id=patient_id)

            Visit.objects.create(
                patient=patient,
                created_by=request.user
            )

            messages.success(request, "Visit started successfully.")

            return redirect("triage_dashboard")  # Redirect to the triage page after starting the visit

    return render(
        request,
        "start_visit.html",
        {
            "patient": patient
        }
    )
   
def triage_dashboard(request):
    triage_waiting_visits = Visit.objects.filter(status="waiting", current_department="triage")
    return render(request, "triage_dashboard.html", {"visits": triage_waiting_visits})

def triage(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)
    if request.method == "POST":
        form = TriageForm(request.POST)
        if form.is_valid():
            triage = form.save(commit=False)
            triage.visit = visit
            triage.save()
            visit.current_department = "doctor"
            visit.status = "waiting"
            visit.save()
            messages.success(request, "Triage information saved successfully.")
            return redirect("triage_dashboard")  # Redirect to a success page or another view
    else:
        form = TriageForm()
        messages.error(request, "Please correct the errors below.")
    return render(request, "triage.html", {"form": form, "visit": visit})

def doctor_consultation(request, visit_id):

    visit = get_object_or_404(
        Visit,
        id=visit_id
    )

    # Patient is now being served
    if visit.status == "waiting":
        visit.status = "serving"
        visit.save(update_fields=["status"])

    if request.method == "POST":

        form = DoctorConsultationForm(request.POST)

        if form.is_valid():

            consultation = form.save(commit=False)

            consultation.visit = visit
            consultation.consulted_by = request.user

            consultation.save()

            visit.current_department = consultation.next_department

            if consultation.next_department == "completed":
                visit.status = "completed"
            else:
                visit.status = "waiting"

            visit.save()

            messages.success(
                request,
                "Consultation completed successfully."
            )

            return redirect("doctor_dashboard")

    else:

        form = DoctorConsultationForm()

    return render(
        request,
        "doctor_consultation.html",
        {
            "visit": visit,
            "form": form,
        }
    )


def triage_tv(request):

    serving = Visit.objects.filter(
        current_department="triage",
        status="serving"
    ).first()

    waiting = Visit.objects.filter(
        current_department="triage",
        status="waiting"
    ).order_by("visit_date")

    return render(
        request,
        "triage_tv.html",
        {
            "serving": serving,
            "waiting": waiting,
        },
    )
    
    
def doctor_tv(request):

    serving = Visit.objects.filter(
        current_department="doctor",
        status="serving"
    ).first()

    waiting = Visit.objects.filter(
        current_department="doctor",
        status="waiting"
    ).order_by("visit_date")

    return render(
        request,
        "doctor_tv.html",
        {
            "serving": serving,
            "waiting": waiting,
        },
    )