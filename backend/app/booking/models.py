from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..boat.models import Boat
from ..event.models import Event
from ..mail.models import Mail
from ..transaction.models import Transaction

User = get_user_model()


class Booking(models.Model):
    from_date_time = models.DateTimeField()
    until_date_time = models.DateTimeField()
    
    # remove blank and null? => delete db ;P
    duration = models.DurationField(blank=True, null=True)
    duration_weekday = models.DurationField(blank=True, null=True)
    duration_weekend = models.DurationField(blank=True, null=True)
    user = models.ForeignKey(to=User, related_name='bookings', on_delete=models.SET_NULL, null=True)
    boat = models.ForeignKey(to=Boat, related_name='bookings', on_delete=models.SET_NULL, null=True)
    event = models.OneToOneField(to=Event, related_name='bookings', on_delete=models.SET_NULL,
                                 blank=True, null=True)
    transaction = models.OneToOneField(to=Transaction, related_name='booking', on_delete=models.SET_NULL,
                                       blank=True, null=True)

    def __str__(self):
        return f'ID{self.id}: from {self.from_date_time} to: {self.until_date_time}'


@receiver(post_save, sender=Booking)
def send_email(sender, instance, **kwargs):

    email = Mail(recipient=instance.user.email,
                 subject='Buchungsbestätigung sailcom.ch',
                 content=f'Boot: {instance.boat.id}')
    email.save()


@receiver(post_save, sender=Booking)
def create_trans(sender, instance, created, **kwargs):
    test = 'test'
    price = float(Boat.objects.get(id=instance.boat.id).price_hour_weekday)*float(instance.duration.seconds/60/60)
    #(instance.duration.seconds/60/60)
    Transaction.objects.create(sent=False, price=price, booking=instance, user=instance.user)

