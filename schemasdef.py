import datetime
import graphene
from neotime import DateTime


class CustomGrapheneDateTime(graphene.DateTime):
    @staticmethod
    def serialize(date):
        if isinstance(date, DateTime):
            date = datetime.datetime(date.year, date.month, date.day,
                                     date.hour, date.minute, int(date.second),
                                     int(date.second * 1000000 % 1000000),
                                     tzinfo=date.tzinfo)
        return graphene.DateTime.serialize(date)


class PersonSchema(graphene.ObjectType):
    key = graphene.String()
    name = graphene.String()
    bio = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class PersonInput(graphene.InputObjectType):
    key = graphene.String(required=True)
    name = graphene.String()
    bio = graphene.String()
    email = graphene.String()
    phone = graphene.String()


class TweetSchema(graphene.ObjectType):
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class TweetQuerySchema(graphene.ObjectType):
    key = graphene.Int()
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class TweetInput(graphene.InputObjectType):
    text = graphene.String()
    timestamp = CustomGrapheneDateTime()


class TweetDeleteInput(graphene.InputObjectType):
    key = graphene.Int()


# Following relationship
class FollowingInput(graphene.InputObjectType):
    person_key = graphene.String(required=True)
    follower_key = graphene.String(required=True)


# Person Tweet relationship
class PersonTweetInput(graphene.InputObjectType):
    person_key = graphene.String(required=True)
    tweet_key = graphene.Int(required=True)
