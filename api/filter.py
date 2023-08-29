import django_filters
from . import models


class CourseFilter(django_filters.FilterSet):
    category = django_filters.ChoiceFilter(
        field_name="category",
        choices=models.CHOICES,
        null_label='Uncategorized',
    )

    class Meta:
        model = models.Course
        fields = {
            'category': ['exact'],
        }