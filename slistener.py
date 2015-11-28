from tweepy import StreamListener
import json, time, sys


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api or API()
        self.counter = 0
        self.fprefix = fprefix
        self.name=fprefix + '.' + time.strftime('%d-%m-%Y___%H-%M-%S') + '.json'
        self.t1=time.time()
        self.output  = open(self.name, 'w')
        self.delout  = open('delete.txt', 'a')
        self.lg      = open('log.txt','a')
        self.elg      = open('elog.txt','a')
        #print 'terminated 1'

    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
            #print 'gg'
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            #print 'terminated 3'
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            #print 'terminated 4'
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            #print 'terminated 5'
            warning = json.loads(data)['warnings']
            print warning['message']
            return false

    def on_status(self, status):
        self.output.write(status + "\n")

        self.counter += 1
        #print self.counter

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../streaming_data/' + self.fprefix + '.'
                               + time.strftime('%d-%m-%Y___%H-%M-%S') + '.json', 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        #print 'terminated 6'
        self.delout.write( str(status_id) + "\n")
        return

    def on_limit(self, track):
        #print 'terminated 7'
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        #print 'terminated 8'
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        num=0
        f=open(self.name,'r')
        for line in f:
          try:
            num=num+1
          except:
            pass
        self.lg.write(time.strftime('%d-%m-%Y___%H-%M-%S')+'     Tweets:'+' '+str(num/2)+"\n")
        #self.elg.write('Error:\n'+str(status_code)+'\n'+'Tweets: '+str(num/2+1)+'   Runime: '+str(t)+'\n')
        t2=time.time()
        t=t2-self.t1
        self.elg.write(time.strftime('%d-%m-%Y___%H-%M-%S')+'\n'+'Error: ' + str(status_code)+'\n'+'Tweets: '+str(num/2)+'   Runime: '+str(t)+'\n\n')
        return False




    def on_timeout(self):
        #print 'terminated 9'
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
