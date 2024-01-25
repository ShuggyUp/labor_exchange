import factory
from models import Job
from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user_id = factory.Faker("pyint")
    title = factory.Faker("job")
    description = factory.Faker("pystr")
    salary_from = factory.Faker("pyfloat", min_value=0, max_value=10000)
    salary_to = factory.Faker("pyfloat", min_value=10000, max_value=100000)
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)
