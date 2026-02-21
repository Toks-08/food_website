from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        menu_item_id = self.request.query_params.get('menu_item')

        if menu_item_id:
            return Review.objects.filter(menu_item_id=menu_item_id)

        return Review.objects.all()