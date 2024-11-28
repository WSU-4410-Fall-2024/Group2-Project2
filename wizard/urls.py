from django.urls import path, include
from django.views.generic import RedirectView
from . import views
urlpatterns = [
    path('', RedirectView.as_view(url='/about/', permanent=False), name='index'),
    path('about/',views.about,name='about'),

    path('reservations/', views.reservations, name='reservations'),
    path('reservations/<int:reservation_id>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('contact/',views.contact,name='contact'),

    path('events/', views.events_view, name='events'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/comment/', views.add_comment, name='add_comment'),
    path('comments/<int:comment_id>/reply/', views.reply_comment, name='reply_comment')
]
