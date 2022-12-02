import factory
from faker import Faker
from Auth.models import User
from Blog.models import BlogPost


faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = faker.unique.name()
    email = faker.unique.email()
    password = factory.PostGenerationMethodCall(
        'set_password', 'pAssw0rd1'
    )
    is_staff = factory.Sequence(lambda n: False)
    is_activated = factory.Sequence(lambda n: False)

    @factory.post_generation
    def is_staff(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.is_staff = True

    @factory.post_generation
    def is_activated(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.is_activated = True


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BlogPost

    owner = factory.SubFactory(UserFactory)
    title = faker.name()
    description = faker.text()
    email = faker.email()
    phone_number = faker.phone_number()
