import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django_tenants.utils import schema_context

# Setup Django if standalone (though running via manage.py shell is easier)

def test_form():
    from recruitment.models import Recruitment, JobPosition, Candidate
    from recruitment.forms import CandidateCreationForm
    # Also try to import CandidateDropDownForm if it exists
    try:
        from recruitment.forms import CandidateDropDownForm
        print("Found CandidateDropDownForm")
        FormClass = CandidateDropDownForm
    except ImportError:
        print("CandidateDropDownForm NOT found, using CandidateCreationForm")
        FormClass = CandidateCreationForm

    with schema_context('testco11'):
        recruitment = Recruitment.objects.filter(title="Hiring HR Manager").first()
        if not recruitment:
            print("Recruitment not found!")
            return

        job_position = recruitment.open_positions.first()
        if not job_position:
            print("Job Position not found!")
            return

        print(f"Testing Form with Recruitment: {recruitment} (Optional Resume: {recruitment.optional_resume})")
        print(f"Job Position: {job_position}")

        # Simulate file upload
        resume_file = SimpleUploadedFile("resume.pdf", b"file_content", content_type="application/pdf")
        
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "mobile": "1234567890",
            "recruitment_id": recruitment.id,
            "job_position_id": job_position.id,
            "profile": "", 
            "source": "website", # Still might be invalid, checking choices? Default is "software"?
            "gender": "male", # Check choices
            "dob": "1990-01-01",
            "address": "123 St",
            "country": "US",
            "state": "NY",
            "zip": "10001",
        }
        files = {
            "resume": resume_file
        }

        form = FormClass(data=data, files=files)
        
        # We need to mimic the instance behavior if the form relies on it
        # ModelForm creates instance from data usually.
        
        if form.is_valid():
            print("Form is VALID")
        else:
            print("Form is INVALID")
            print(form.errors)

        # Test Case 2: No Resume
        print("\nTesting WITHOUT Resume:")
        files_no_resume = {}
        form2 = FormClass(data=data, files=files_no_resume)
        if form2.is_valid():
            print("Form 2 is VALID")
        else:
            print("Form 2 is INVALID")
            print(form2.errors)

test_form()
