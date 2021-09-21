from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated, IsAdminUser,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from .filters import TitleFilter
from .models import Title, Category, Genre, Comment, Review
from .permissions import ReadOnly, ReviewCommentPermission
from .serializer import (SignUpSerializer, TokenSerializer, TitleSerializer,
                         TitlePostSerializer, GenreSerializer,
                         CategoryListSerializer, ReviewSerializer,
                         CommentSerializer)
from .utils import send_token_for_user


class SignUpApiView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, _ = User.objects.get_or_create(
            email=email, username=username,
            is_active=False
        )
        send_token_for_user(request, user)

        return Response({'email': email}, status=status.HTTP_200_OK)


class EmailConfirmationView(APIView):
    serializer_class = TokenSerializer

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, email=serializer.data['email'])
        confirmation_code = serializer.data['confirmation_code']
        if default_token_generator.check_token(user, confirmation_code):
            user.is_active = True
            user.save()
            token = self.get_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)

        response = {'confirmation_code': 'invalid confirmation code'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('rating')

    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer


class BaseCreateViewSet(mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    pass


class GenreViewSet(BaseCreateViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['=name']


class CategoryViewSet(BaseCreateViewSet):
    serializer_class = CategoryListSerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated & IsAdminUser | ReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    lookup_field = 'slug'
    search_fields = ['=name']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReviewCommentPermission
    )
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title__pk=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        ReviewCommentPermission
    )

    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__pk=title_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return Comment.objects.filter(review=review)
