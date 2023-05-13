from polyfactory.factories import pydantic_factory


def generate_fake_data(basemodel_class):
    """Fills in a basemodel with random data based on type hints"""

    class Factory(pydantic_factory.ModelFactory[basemodel_class]):
        __model__ = basemodel_class

    return Factory.build().dict()
