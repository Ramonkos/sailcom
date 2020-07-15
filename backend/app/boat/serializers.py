from rest_framework import serializers

from .boat_document.serializers import DocumentSerializer
from .image.serializers import ImageSerializer
from .models import Boat
from ..boat_crew.serializers import BoatCrewSerializer
from ..mooring.serializers import MooringSerializer
from .image.serializers import ImageSerializer


class BoatSerializer(serializers.ModelSerializer):
    crew = BoatCrewSerializer(read_only=True)

    images = ImageSerializer(read_only=True, many=True)
    boat_documents = DocumentSerializer(read_only=True, many=True)
    mooring = MooringSerializer(read_only=True)

    class Meta:
        model = Boat
        fields = ['id', 'title', 'price_hour_weekday', 'price_hour_weekend', 'price_fullday_weekday',
                  'price_fullday_weekend', 'description', 'a_license_required',
                  'length', 'width', 'draught', 'max_crew', 'recommended_crew', 'mooring',
                  'model', 'crew', 'images', 'boat_documents']
