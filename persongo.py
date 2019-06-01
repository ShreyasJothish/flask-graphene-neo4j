from py2neo.ogm import GraphObject, Property
from py2neo.ogm import RelatedTo, RelatedFrom


class Person(GraphObject):
    __primarykey__ = "key"

    key = Property()
    name = Property()
    bio = Property()
    email = Property()
    phone = Property()

    # Set of Person whom the Person follows
    followings = RelatedTo("Person", "FOLLOWINGS")

    # Set of Person who follow the Person
    followers = RelatedFrom("Person", "FOLLOWERS")

    # Set of Tweets posted by Person
    posted_tweets = RelatedTo("Tweet")

    def add_or_update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __init__(self, **kwargs):
        self.add_or_update(**kwargs)

    def as_dict(self):
        return {
            'key': self.key,
            'name': self.name,
            'bio': self.bio,
            'email': self.email,
            'phone': self.phone,
        }

    def update(self, **kwargs):
        self.add_or_update(**kwargs)

    # List interfaces
    def add_or_update_followings(self, followings):
        for following in followings:
            self.followings.update(following)

    def add_or_update_following(self, following):
        self.followings.update(following)

    def remove_followings(self, followings):
        for following in followings:
            self.followings.remove(following)

    def remove_following(self, following):
        self.followings.remove(following)

    def add_or_update_followers(self, followers):
        for follower in followers:
            self.followers.update(follower)

    def add_or_update_follower(self, follower):
        self.followers.update(follower)

    def remove_followers(self, followers):
        for follower in followers:
            self.followers.remove(follower)

    def remove_follower(self, follower):
        self.followers.remove(follower)

    def add_or_update_posted_tweets(self, tweets):
        for tweet in tweets:
            self.posted_tweets.update(tweet)

    def add_or_update_posted_tweet(self, tweet):
        self.posted_tweets.update(tweet)

    def remove_posted_tweets(self, tweets):
        for tweet in tweets:
            self.posted_tweets.remove(tweet)

    def remove_posted_tweet(self, tweet):
        self.posted_tweets.remove(tweet)

    # Object level interfaces
    def save(self, graph):
        graph.push(self)

    def delete(self, graph):
        graph.delete(self)


# To avoid cyclic dependency import error
from tweetgo import Tweet  # noqa: E402 F401
