from django.urls import path

from .views import (
    candidate_profile,
    request_job,
    candidate_requests,
    cancel_request,
)

urlpatterns = [
    path("profile/", candidate_profile, name="candidate-profile"),
    path("request/job/<slug:slug>/", request_job, name="request-job"),
    path("requests/", candidate_requests, name="candidate-requests"),
    path("cancel/request/<slug:slug>/", cancel_request, name="cancel-request"),
]
