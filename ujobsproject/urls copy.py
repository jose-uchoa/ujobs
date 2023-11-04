from django.contrib import admin
from django.urls import path, include

# from django.conf import settings
# from django.conf.urls.static import static

from core.views import (
    register,
    login_request,
    home_page,
    job_detail,
    search,
)


urlpatterns = [
    path("", home_page, name="home-page"),
    path("admin/", admin.site.urls),
    path("candidate/", include("candidate.urls")),
    path("company/", include("company.urls")),
    path("register/", register, name="register"),
    path("login/", login_request, name="login"),
    path("job/<slug:slug>/", job_detail, name="job-detail"),
    path("search/", search, name="search"),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
