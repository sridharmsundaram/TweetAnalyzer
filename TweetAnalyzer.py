import re
import tweepy
import nltk
from tweepy import OAuthHandler
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer

class TweetAnalyzer(object):
	'''
	Generic Twitter Class for sentiment analysis.
	'''
	def __init__(self):
		'''
		Class constructor or initialization method.
		'''
		# keys and tokens from the Twitter Dev Console
		consumer_key = '<<Consumer Key>>'
		consumer_secret = '<<Consumer Secret>>'
		access_token = '<<Access Token>>'
		access_token_secret = '<<Access Token Secret>>'

		# attempt authentication
		try:
			# create OAuthHandler object
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			# set access token and secret
			self.auth.set_access_token(access_token, access_token_secret)
			# create tweepy API object to fetch tweets
			self.api = tweepy.API(self.auth)
		except:
			print("Error: Authentication Failed")

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def get_tweets(self, query, count = 10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search_tweets(q = query, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

	def stemming_on_text(data):
		text = [st.stem(word) for word in data]
		return data

def main():

	# creating object of TwitterClient Class
	api = TweetAnalyzer()
	# calling function to get tweets
	strQuery = 'COVID19 pandemic'
	tweets = api.get_tweets(query = strQuery, count = 2000)
	try:
		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		# percentage of positive tweets
		#print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
		#fstringle=i
		ptweetPercent = round(100 * len(ptweets) / len(tweets),1)
		#f"Positive tweets percentage: ,{ptweetPercent}%"
		print("Positive tweets percentage: {} %".format(ptweetPercent))
		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		# percentage of negative tweets
		ntweetPercent = round(100*len(ntweets)/len(tweets),1)
		#f"Negative tweets percentage: ,{ntweetPercent}%"
		print("Negative tweets percentage: {} %".format(ntweetPercent))
		# percentage of neutral tweets
		neutralTweetPercent = round(100 - (ptweetPercent + ntweetPercent),1)
		#f"Neutral tweets percentage: ,{neutralTweetPercent}%"
		print("Neutral tweets percentage: {} % ". format(neutralTweetPercent))
		#print("Neutral tweets percentage: {} % \
		#	".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets)))

		# printing first 5 positive tweets
		print("\n\nPositive tweets:")
		for tweet in ptweets[:10]:
			print(tweet['text'])

		# printing first 5 negative tweets
		print("\n\nNegative tweets:")
		for tweet in ntweets[:10]:
			print(tweet['text'])

	except:
		print("\n No tweets found for the search criteria: " + strQuery)



	# tokenizer = RegexpTokenizer(r'w+')
	# ptweets['text'] = ptweets['text'].apply(tokenizer.tokenize)
	# ptweets['text'].head()
	#
	# st = nltk.PorterStemmer()



	#dataset['text'] = dataset['text'].apply(lambda x: stemming_on_text(x))
	#dataset['text'].head()

if __name__ == "__main__":
	# calling main function
	main()
