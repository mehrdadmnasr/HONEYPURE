from django.conf.urls.i18n import i18n_patterns
from django.urls import path

urlpatterns = [
    # سایر URLها
]

urlpatterns += i18n_patterns(
    path('your-url/', include('your_app.urls')),
)
