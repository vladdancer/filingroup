from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.pagination import PageNumberPagination

from about_us.models import AboutModel
from courses.models import Teacher, Discount, CourseTypes, Course, Privilege, Student, CourseReview
from blog.models import Category, Tag, Post, Comment
from sending_agreement.models import Agreement
from privacy_policy.models import PrivacyPolicy
from site_rules.models import SiteRule
from denial.models import Denial
from take_access.models import Access
from .serializers import AboutUsSerializer, TeacherSerializer, DiscountSerializer, CourseTypesSerializer,\
    CourseSerializer, PrivilegeSerializer, StudentSerializer, CourseReviewSerializer, CategoryBlogSerializer,\
    TagSerializer, PostSerializer, CommentSerializer, AgreementSerializer, PrivacyPolicySerializer,\
    SiteRuleSerializer, DenialSerializer, AccessSerializer


# Take access viewset
class AccessViewSet(CreateAPIView):
    queryset = Access.objects.all()
    serializer_class = AccessSerializer


# About us viewsets
class AboutUsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing About objects
    """
    queryset = AboutModel.objects.all()
    serializer_class = AboutUsSerializer


# Courses views/viewsets
class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Teacher objects
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer


class CourseTypesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing CourseTypes objects
    """
    queryset = CourseTypes.objects.filter(is_active=True)
    serializer_class = CourseTypesSerializer


class CourseListView(ListAPIView):
    """
    API endpoint for listing Courses objects
    """
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for displaying single Course objects
    """
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer
    lookup_field = 'slug'


class PrivilegeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Privilege objects
    """
    queryset = Privilege.objects.all()
    serializer_class = PrivilegeSerializer


class StudentCreateListViewSet(mixins.CreateModelMixin,
                               mixins.UpdateModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    """
    API endpoint for listing, creating and updating Student objects
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        student = serializer.save()

        # setting course
        try:
            courses = str(self.request.data['courses'])
        except:
            courses = ""
        if courses:
            courses = Course.objects.get(id=courses)
            student.courses = courses
        student.save()


class CourseReviewViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    """
    API endpoint for listing and creating CourseReview objects
    """
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer

    def perform_create(self, serializer):
        review = serializer.save()

        try:
            course = str(self.request.data['course'])
        except:
            course = ""
        if course:
            course = Course.objects.get(id=course)
            review.course = course
        review.save()


# Blog views/viewsets
class CategoryBlogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Category objects
    """
    queryset = Category.objects.all()
    serializer_class = CategoryBlogSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Tag objects
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostListView(ListAPIView):
    """
    API endpoint for listing Post objects
    """
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = super(PostListView, self).get_queryset()

        category = self.kwargs.get('category')
        if category:
            category = Category.objects.get(slug=category)
            return query.filter(category=category)

        return query


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    lookup_field = 'slug'


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Comment objects
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


# Sending agreement viewsets
class AgreementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Agreement objects
    """
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer


# Privacy Policy viewsets
class PrivacyPolicyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing PrivacyPolicy objects
    """
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer


# Site Rules viewsets
class SiteRulesViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing SiteRule objects
    """
    queryset = SiteRule.objects.all()
    serializer_class = SiteRuleSerializer


# Denial viewsets
class DenialViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing Denial objects
    """
    queryset = Denial.objects.all()
    serializer_class = DenialSerializer
