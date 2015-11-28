from slistener import SListener
import time, tweepy, sys,os
import csv

def createdir():
	directoryName=time.strftime('%d-%m-%y__%H-%M-%S')
	os.mkdir(directoryName)
	os.chdir(directoryName)

def authenticate():
	consumer_key='xzVYpnUFkuzg3gNtHqrNwGYXu'
	consumer_secret='d1EepDVjnpQOD5BHIq6w5QafYoAo64Le5zdDLZf0tuxb9j5TVL'
	access_secret='61731772-QQqru4iCPqP7csv7RMdGV8qtOmz4zZ396gXO8S38Y'
	access_token_secret='cVDlWy3kyyFjW8l7DpmDF0GjBLMY1EFLj99DONXX1zOFp'
	return consumer_key,consumer_secret,access_secret,access_token_secret

def get_tweets(screen_name):

	createdir()
	consumer_key,consumer_secret,access_token,access_token_secret = authenticate()   

	ta=time.time()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.secure = True
	auth.set_access_token(access_token, access_token_secret)
	total=0

	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	
	pass       

        
if __name__=='__main__':
	get_tweets("narendramodi")


