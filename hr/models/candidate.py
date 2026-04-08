 
from django.db import models
from core.models import BaseModel

class CandidateStatusChoices(models.TextChoices):
    APPLIED = 'Applied', 'Applied'
    IN_REVIEW = 'In Review', 'In Review'
    INTERVIEW_SCHEDULED = 'Interview Scheduled', 'Interview Scheduled'
    OFFERED = 'Offered', 'Offered'
    REJECTED = 'Rejected', 'Rejected'


class Candidate(BaseModel):
    vacancy = models.ForeignKey('Vacancy', on_delete=models.CASCADE, related_name='candidates')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    resume = models.FileField(upload_to='candidates/resumes/', null=True, blank=True)
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True , choices=CandidateStatusChoices.choices)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recruiter = models.CharField(max_length=255, blank=True, null=True)  # Name of the recruiter handling this candidate
    interviwer = models.CharField(max_length=255, blank=True, null=True)  # Name of the interviewer assigned to this candidate
    notes = models.TextField(blank=True, null=True)  # Additional notes about the candidate
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Candidate's expected salary
    source_channel = models.CharField(max_length=255, blank=True, null=True)  # How the candidate found out about the vacancy (e.g., LinkedIn, referral, job board)
    
    class Meta:
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
        app_label = 'hr'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} applying for {self.vacancy.position.title}"

