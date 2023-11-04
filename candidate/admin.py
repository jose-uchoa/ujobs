from django.contrib import admin

from .models import CandidateProfile, CandidateRequests

admin.site.register(CandidateProfile)
admin.site.register(CandidateRequests)
