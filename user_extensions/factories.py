from django.contrib.auth import get_user_model
import factory
import factory.fuzzy


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.fuzzy.FuzzyText()
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
