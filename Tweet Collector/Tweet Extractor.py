

#libraries used
import pandas as pd
import tweepy

#python file containing consumer keys and access tokens
import TweeKeys

# function to display data of each tweet
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Tweet Text:{ith_tweet[0]}")


# function to perform data extraction
def scrape(words, numtweet):
    # Creating DataFrame using pandas
    db = pd.DataFrame(columns=['text'])

    consumer_key = TweeKeys.CONSUMER_KEY
    consumer_secret = TweeKeys.CONSUMER_SECRET
    access_key = TweeKeys.ACCESS_TOKEN
    access_secret = TweeKeys.ACCESS_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    tweets = tweepy.Cursor(api.search, q=words, lang="fil", tweet_mode='extended').items(numtweet)


    list_tweets = [tweet for tweet in tweets]

    # Counter to maintain Tweet Count
    i = 1

    # we will iterate over each tweet in the list for extracting information about each tweet
    for tweet in list_tweets:
        hashtags = tweet.entities['hashtags']

        # Retweets can be distinguished by a retweeted_status attribute,
        # in case it is an invalid reference, except block will be executed
        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:
            text = tweet.full_text
        hashtext = list()
        for j in range(0, len(hashtags)):
            hashtext.append(hashtags[j]['text'])

        # Here we are appending all the extracted information in the DataFrame
        ith_tweet = [text]
        db.loc[len(db)] = ith_tweet

        # Function call to print tweet data on screen
        printtweetdata(i, ith_tweet)
        i = i + 1



    # print to csv function
    fname = 'Training_setV4.csv'
    db.to_csv(fname)


if __name__ == "__main__":

    # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()


    # number of tweets you want to extract in one run
    numtweet = 6000
    scrape(words, numtweet)
    print('Scraping has completed!')