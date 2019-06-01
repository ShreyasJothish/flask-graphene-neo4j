from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedFrom


class Tweet(GraphObject):

    text = Property()
    timestamp = Property()

    # Comment posted by a Person
    poster = RelatedFrom("Person", "COMMENT_POSTED")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'key': self.__primaryvalue__,
            'text': self.text,
            'timestamp': self.timestamp
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_poster(self, poster):
        self.poster.update(poster)

    def remove_poster(self, poster):
        self.poster.remove(poster)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from persongo import Person  # noqa: E402 F401
