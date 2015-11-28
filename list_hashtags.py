import csv, json, pickle

def getHashIndex(hash_tag,list_hash_tags):
	
	hash_tag_index = -1
	
	for word in list_hash_tags:
		if(word == hash_tag):
			hash_tag_index = list_hash_tags.index(word)
			break
	
	#if user is not already present create an entry for the user in list_user
	if(hash_tag_index==-1):
		list_hash_tags.append(hash_tag)		
		hash_tag_index = len(list_hash_tags)-1
		
	return hash_tag_index, list_hash_tags
	

def getUserIndex(data,user_name):

	#get index if username is already present
	with open('pickle_tweet_username','r') as f:
		list_user = pickle.load(f)
	
	user_index = -1
	
	for user in list_user:
		if(user == user_name):
			user_index = list_user.index(user)
			break
	
	#if user is not already present create an entry for the user in list_user
	if(user_index==-1):
		list_user.append(user_name)	
		user_index = len(list_user)-1
		data.append([[]])
	
	#dump list_user
	with open('pickle_tweet_username','w') as f:
		pickle.dump(list_user,f)
		
	return user_index

def update_matrix(data,user_name,hash_tags,tweet_id):
	#data is a 3d list
	#username is a string
	#hash_tags is list of strings
	#tweet_id is string
	
	user_index = getUserIndex(data,user_name)
	
	#load pickle of list containing hash_tags
	with open('pickle_tweet_hashtags','r') as f:
		list_hash_tags = pickle.load(f)
	
	for tag in hash_tags:
		col_id,list_hash_tags = getHashIndex(tag,list_hash_tags)
		#update the entry in data
		if(col_id > len(data[user_index])-1):
			for n in range(0,col_id-(len(data[user_index])-1)):
				data[user_index].append([])
				
		#print len(data),len(data[user_index]),user_index,col_id

		data[user_index][col_id].append(tweet_id)
		
		
	#dump list_hash_tags
	with open('pickle_tweet_hashtags','w') as f:
		pickle.dump(list_hash_tags,f)
	

def hash_list(row):
	#row is string of strings
	tweet_id = row[0]
	tweet = row[2]
	hashtags = [word[1:] for word in tweet.split() if word[0] == '#']
	set(hashtags)
	hashtags = list(hashtags)
	#returning tweet_id and hashtags (list of hashtags which are string objects)
	return tweet_id,hashtags  


def list_hashtags(file_name):
	#defining username which is the source of tweet
	user_name = file_name
	
	#read file with all downloaded tweets
	f = open(file_name+".csv",'rt')
	reader=csv.reader(f)
	
	#load the pickle dump of tweet_matrix
	with open('pickle_tweet.data','r') as f_pickle:
		data = pickle.load(f_pickle)	
	
	#reading file line by line
	try:
		reader=csv.reader(f)
		for row in reader:
			#each row is read in the form of string of strings
			
			#passing row to extract all hashtags
			tweet_id,hash_tags = hash_list(row)
			
			#update the tweet matrix with username and
			update_matrix(data,user_name,hash_tags,tweet_id)			
			
	finally:
		f.close()
	
	print data
	
	#dump the pickle dump of tweet_matrix
	with open('pickle_tweet.data','w') as f_pickle:
		pickle.dump(data,f_pickle)
	
	
if __name__=='__main__':
	list_hashtags("list_hashtags")	
	'''
	data1 = [[[]]]
	with open('pickle_tweet.data','w') as f_pickle:
		pickle.dump(data1,f_pickle)
		
	data2 = []
	with open('pickle_tweet_username','w') as f_pickle:
		pickle.dump(data2,f_pickle)
		
	with open('pickle_tweet_hashtags','w') as f_pickle:
		pickle.dump(data2,f_pickle)
	'''
	
	
	

