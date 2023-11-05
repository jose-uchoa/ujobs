from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    company_home,
    company_profile,
    company_jobs,
    company_create_job,
    company_update_job,
    company_delete_job,
    accepted_status,
    hired_status,
    delete_request,
    reject_and_delete_request,
    job_candidates_view,
)


urlpatterns = [
    path("home", company_home, name="company-home"),
    path("profile/", company_profile, name="company-profile"),
    path("jobs/", company_jobs, name="company-jobs"),
    path("create/job/", company_create_job, name="company-create-job"),
    path("job/<slug:slug>/update/", company_update_job, name="company-update-job"),
    path("job/<slug:slug>/delete/", company_delete_job, name="company-delete-job"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("accept/request/<int:request_id>/<slug:slug>/", accepted_status, name="accept-status"),
    path("hire/request/<int:request_id>/<slug:slug>/", hired_status, name="hire-status"),
    path("delete/request/<int:request_id>/<slug:slug>/", delete_request, name="delete-request"),
    path(
        "reject-and-delete/request/<int:request_id>/<slug:slug>/",
        reject_and_delete_request,
        name="reject-and-delete-request",
    ),
    path("job/<slug:slug>/candidates/", job_candidates_view, name='job-candidates'),
]
