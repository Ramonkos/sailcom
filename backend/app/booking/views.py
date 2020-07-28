from django.db.models import Q
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView

from datetime import timedelta, datetime
from django.utils import timezone
from .models import Booking
from .serializers import BookingSerializer, CreateBookingSerializer
from ..boat.models import Boat
from ..permissions import IsLoggedIn, IsStaffOrCreator, MemberPostLoggedInFetch


class ListCreateBookingsView(ListCreateAPIView):
    queryset = Booking.objects.all().order_by('from_date_time')
    permission_classes = [MemberPostLoggedInFetch]

    def get_serializer_class(self):
        if self.request is None:  # for API documentation
            return BookingSerializer
        elif self.request.method == 'POST':  # for creating bookings
            return CreateBookingSerializer
        return BookingSerializer

    def post(self, request, *args, **kwargs):
        if self.request.data.get('until_date_time') is None or self.request.data.get('from_date_time') is None:
            return HttpResponse('Die Daten von und bis sind nicht vollständig', status=400)
        until_date_time = request.data.get('until_date_time')
        from_date_time = request.data.get('from_date_time')

        if from_date_time >= until_date_time:
            res = {
                "Buchungsende ist nicht nach Buchungsanfang"
            }
            return HttpResponse(res, status=400)
        if self.request.data.get('boat') is None:
            return HttpResponse('Bitte Boot auswählen', status=400)
        existing_bookings = Booking.objects.filter(Q(boat__id__exact=self.request.data.get('boat'))) \
            .filter((
                        Q(from_date_time__exact=from_date_time)
                    ) | (
                            Q(from_date_time__gt=from_date_time) &
                            Q(from_date_time__lt=until_date_time)
                    ) | (
                            Q(from_date_time__lt=from_date_time) &
                            Q(until_date_time__gt=from_date_time)
                    ))
        if len(existing_bookings) > 0:
            res = {
                "Das Boot kann zu dieser Zeit nicht gebucht werden"
            }
            return HttpResponse(res, status=400)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.is_valid()

        # calculate booking duration
        until_date_time = serializer.validated_data.get('until_date_time')
        from_date_time = serializer.validated_data.get('from_date_time')
        duration = until_date_time - from_date_time
        less_24 = duration.days == 0

        dt_start = serializer.validated_data.get('from_date_time').date()
        dt_end = serializer.validated_data.get('until_date_time').date()
        dt_current = dt_start
        weekday_count = 0
        weekend_count = 0

        # loop through days to count weekend days and weekdays
        if not less_24:
            while dt_current <= dt_end:
                if dt_current.isoweekday() > 5:
                    weekend_count += 1
                else:
                    weekday_count += 1
                dt_current = dt_current + timedelta(1)  # add 1 day to current day

        serializer.save(
            user=self.request.user,
            duration=duration,
            weekday_days=weekday_count,
            weekend_days=weekend_count
        )


class CalculateBookingView(ListAPIView):
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):
        if self.request.data.get('from_date_time') is None or self.request.data.get('until_date_time') is None:
            return HttpResponse('Die Daten von und bis sind nicht vollständig', status=400)

        until_date_time = datetime.strptime(request.data.get('until_date_time'), '%Y-%m-%dT%H:%M')
        from_date_time = datetime.strptime(request.data.get('from_date_time'), '%Y-%m-%dT%H:%M')

        if from_date_time >= until_date_time:
            res = {
                "Buchungsende ist nicht nach Buchungsanfang"
            }
            return HttpResponse(res, status=400)
        if self.request.data.get('boat') is None:
            res = {
                "Bitte Boot auswählen"
            }
            return HttpResponse(res, status=400)

        duration = until_date_time - from_date_time
        less_24 = duration.days == 0

        dt_start = from_date_time.date()
        dt_end = until_date_time.date()
        dt_current = dt_start
        weekday_count = 0
        weekend_count = 0

        # loop through days to count weekend days and weekdays
        if not less_24:
            while dt_current <= dt_end:
                if dt_current.isoweekday() > 5:
                    weekend_count += 1
                else:
                    weekday_count += 1
                dt_current = dt_current + timedelta(1)  # add 1 day to current day

        if weekday_count is not None:
            if weekday_count + weekend_count == 0:  # hourly rate calculation
                if from_date_time.date().isoweekday() < 6:  # 1-5 Mon-Fri
                    price = float(Boat.objects.get(id=request.data['boat']).price_hour_weekday) * float(
                        duration.seconds / 60 / 60)
                else:
                    price = float(Boat.objects.get(id=request.data['boat']).price_hour_weekend) * float(
                        duration.seconds / 60 / 60)
            else:  # daily rate calculation
                price = weekday_count * float(Boat.objects.get(id=request.data['boat']).price_fullday_weekday) \
                        + weekend_count * float(Boat.objects.get(id=request.data['boat']).price_fullday_weekend)

        return HttpResponse(price, status=200)


class DestroyBookingView(DestroyAPIView):
    queryset = Booking.objects.all()
    permission_classes = [IsStaffOrCreator]


class MyBookingView(ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [IsLoggedIn]

    def get_queryset(self):
        data = Booking.objects.filter(Q(user=self.request.user))
        if self.request.query_params.get('mitsegeln') is not None and self.request.query_params.get('mitsegeln') \
                == 'true':
            data = data.filter(from_date_time__gte=timezone.localtime() - timedelta(days=1), event__isnull=True)
        return data.order_by('from_date_time')
