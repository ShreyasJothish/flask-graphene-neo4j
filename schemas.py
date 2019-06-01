import graphene
import os
from py2neo import Graph

# Internal imports
from tweetgo import Tweet
from persongo import Person
from schemasdef import PersonSchema, PersonInput,\
    FollowingInput, TweetSchema, TweetQuerySchema,\
    TweetInput, TweetDeleteInput, PersonTweetInput

# Environment variables
url = os.environ['NEO4J_URL']
username = os.environ['NEO4J_USERNAME']
password = os.environ['NEO4J_PASSWORD']

# Global variables
graph = Graph(url, auth=(username, password))


class CreatePerson(graphene.Mutation):

    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_data=None):
        person = Person(key=person_data.key,
                        name=person_data.name,
                        bio=person_data.bio,
                        email=person_data.email,
                        phone=person_data.phone)
        person.save(graph)
        ok = True

        return CreatePerson(person=person, ok=ok)


class CreateTweet(graphene.Mutation):

    class Arguments:
        tweet_data = TweetInput(required=True)

    tweet = graphene.Field(TweetSchema)
    key = graphene.Int()
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, tweet_data=None):
        tweet = Tweet(text=tweet_data.text,
                      timestamp=tweet_data.timestamp)

        # To get the unique key, first need to store in DB
        tweet.save(graph)

        key = tweet.__primaryvalue__

        ok = True

        return CreateTweet(tweet=tweet, key=key, ok=ok)


# Establish following
class LinkFollowing(graphene.Mutation):

    class Arguments:
        following_data = FollowingInput(required=True)

    person = graphene.Field(PersonSchema)
    follower = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, following_data=None):
        person = Person.match(graph, following_data.person_key).first()
        follower = Person.match(graph, following_data.follower_key).first()

        if not person or not follower:
            ok = False
            return LinkFollowing(person=None, follower=None, ok=ok)

        person.add_or_update_follower(follower)
        person.save(graph)

        follower.add_or_update_following(person)
        follower.save(graph)
        ok = True

        return LinkFollowing(person=person, follower=follower, ok=ok)


class DelinkFollowing(graphene.Mutation):

    class Arguments:
        following_data = FollowingInput(required=True)

    person = graphene.Field(PersonSchema)
    follower = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, following_data=None):
        person = Person.match(graph, following_data.person_key).first()
        follower = Person.match(graph, following_data.follower_key).first()

        if not person or not follower:
            ok = False
            return LinkFollowing(person=None, follower=None, ok=ok)

        person.remove_follower(follower)
        person.save(graph)

        follower.remove_following(person)
        follower.save(graph)
        ok = True

        return DelinkFollowing(person=person, follower=follower, ok=ok)


# Relationship between person and tweet posted
class LinkPersonTweet(graphene.Mutation):

    class Arguments:
        person_tweet_data = PersonTweetInput(required=True)

    person = graphene.Field(PersonSchema)
    tweet = graphene.Field(TweetSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_tweet_data=None):
        person = Person.match(graph, person_tweet_data.person_key).first()
        tweet = Tweet.match(graph, person_tweet_data.tweet_key).first()

        if not person or not tweet:
            ok = False
            return LinkPersonTweet(person=None, tweet=None, ok=ok)

        person.add_or_update_posted_tweet(tweet)
        person.save(graph)

        tweet.add_or_update_poster(person)
        tweet.save(graph)
        ok = True

        return LinkPersonTweet(person=person, tweet=tweet, ok=ok)


class DelinkPersonTweet(graphene.Mutation):

    class Arguments:
        person_tweet_data = PersonTweetInput(required=True)

    person = graphene.Field(PersonSchema)
    tweet = graphene.Field(TweetSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_tweet_data=None):
        person = Person.match(graph, person_tweet_data.person_key).first()
        tweet = Tweet.match(graph, person_tweet_data.tweet_key).first()

        if not person or not tweet:
            ok = False
            return LinkPersonTweet(person=None, tweet=None, ok=ok)

        person.remove_posted_tweet(tweet)
        person.save(graph)

        tweet.remove_poster(person)
        tweet.save(graph)
        ok = True

        return DelinkPersonTweet(person=person, tweet=tweet, ok=ok)


class DeletePerson(graphene.Mutation):

    class Arguments:
        person_data = PersonInput(required=True)

    person = graphene.Field(PersonSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, person_data=None):
        person = Person.match(graph, person_data.key).first()

        if not person:
            ok = False
            return DeletePerson(person=None, ok=ok)

        person.delete(graph)
        ok = True

        return DeletePerson(person=person, ok=ok)


class DeleteTweet(graphene.Mutation):

    class Arguments:
        tweet_data = TweetDeleteInput(required=True)

    tweet = graphene.Field(TweetSchema)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, tweet_data=None):
        tweet = Tweet.match(graph, tweet_data.key).first()

        if not tweet:
            ok = False
            return DeleteTweet(tweet=None, ok=ok)

        tweet.delete(graph)
        ok = True

        return DeleteTweet(tweet=tweet, ok=ok)


class Query(graphene.ObjectType):
    person = graphene.Field(PersonSchema, key=graphene.String())
    tweet = graphene.Field(TweetQuerySchema, key=graphene.Int())

    # Query to fetch all followers of a person
    followers = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all followers of a person
    followings = graphene.List(PersonSchema, key=graphene.String())

    # Query to fetch all tweets posted by a person
    person_posted_tweets = graphene.List(TweetQuerySchema,
                                         key=graphene.String())

    # Query to fetch poster of a particular tweet
    tweet_poster = graphene.List(PersonSchema, key=graphene.Int())

    def resolve_person(self, info, key):
        person = Person.match(graph, key).first()

        if not person:
            return None

        return PersonSchema(**person.as_dict())

    def resolve_tweet(self, info, key):
        tweet = Tweet.match(graph, key).first()

        if not tweet:
            return None

        return TweetQuerySchema(**tweet.as_dict())

    def resolve_followers(self, info, key):
        person = Person.match(graph, key).first()

        if not person:
            return None

        return [PersonSchema(**follower.as_dict())
                for follower in person.followers]

    def resolve_followings(self, info, key):
        person = Person.match(graph, key).first()

        if not person:
            return None

        return [PersonSchema(**following.as_dict())
                for following in person.followings]

    def resolve_person_posted_tweets(self, info, key):
        person = Person.match(graph, key).first()

        if not person:
            return None

        return [TweetQuerySchema(**tweet.as_dict())
                for tweet in person.posted_tweets]

    def resolve_tweet_poster(self, info, key):
        tweet = Tweet.match(graph, key).first()

        if not tweet:
            return None

        return [PersonSchema(**person.as_dict())
                for person in tweet.poster]


class Mutations(graphene.ObjectType):
    create_person = CreatePerson.Field()
    delete_person = DeletePerson.Field()

    create_tweet = CreateTweet.Field()
    delete_tweet = DeleteTweet.Field()

    link_following = LinkFollowing.Field()
    delink_following = DelinkFollowing.Field()

    link_person_tweet = LinkPersonTweet.Field()
    delink_person_tweet = DelinkPersonTweet.Field()


schema = graphene.Schema(query=Query,
                         mutation=Mutations,
                         auto_camelcase=False)
