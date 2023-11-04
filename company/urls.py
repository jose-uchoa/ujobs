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
    reject_request,
    reject_and_delete_request,
)


urlpatterns = [
    path("home", company_home, name="company-home"),
    path("profile/", company_profile, name="company-profile"),
    path("jobs/", company_jobs, name="company-jobs"),
    path("create/job/", company_create_job, name="company-create-job"),
    path("job/<slug:slug>/update/", company_update_job, name="company-update-job"),
    path("job/<slug:slug>/delete/", company_delete_job, name="company-delete-job"),
    path("accept/request/<slug:slug>/", accepted_status, name="accept-status"),
    path("hire/request/<slug:slug>/", hired_status, name="hire-status"),
    path("delete/request/<slug:slug>/", delete_request, name="delete-request"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("reject/request/<slug:slug>/", reject_request, name="reject-request"),
    path(
        "reject-and-delete/request/<slug:slug>/",
        reject_and_delete_request,
        name="reject-and-delete-request",
    ),
]
