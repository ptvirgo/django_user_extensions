import pytz

from django.contrib.auth import get_user_model
import factory
import factory.fuzzy


from .models import ExtendedUserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.fuzzy.FuzzyText()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')


class ProfileFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ExtendedUserProfile

    user = factory.SubFactory(UserFactory)
    country = factory.fuzzy.FuzzyChoice(pytz.country_names)
    timezone = factory.fuzzy.FuzzyChoice(pytz.all_timezones)
