import csv

pos = open("positive-words.txt","r")
neg = open("negative-words.txt","r")

pos_words = pos.read()
neg_words = neg.read()

pos_words = pos_words.split()
neg_words = neg_words.split()

#Open file containing the tweets 
f = open('sample.csv','rt')
reader = csv.reader(f)

#Open file for writing cleaned data
f2 = open('result.csv','wb')

wr = csv.writer(f2, quoting= csv.QUOTE_ALL)

for sentence in reader:
  pcount = 0
  ncount = 0

  sent = sentence[2].lower().split()
  for word in sent:
    if word in pos_words:
      pcount = pcount + 1
    elif word in neg_words:
      ncount = ncount + 1

  if pcount >= ncount and pcount!=0:
    cls = "+1"
  elif ncount>pcount:
    cls = "-1"
  else:
    cls = "0"

  wr.writerow([sentence[0],sentence[1],sentence[2],cls])

