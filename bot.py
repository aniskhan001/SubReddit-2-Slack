import praw
import time
import datetime
import slackweb
from os import environ
# from pymongo import MongoClient

r = praw.Reddit(user_agent = "/r/Futurology/ scraper by aniskhan001")
s = slackweb.Slack(url = environ.get('WEBHOOK_URL'))

cache = []

def run_bot():
	the_time = time.mktime( datetime.datetime.utcnow().timetuple() )
	submissions = r.get_subreddit('Futurology').get_hot(limit=3)

	for sub in submissions:
		# The Top post is over 15 hours old OR less than 750 upvotes
		if ( the_time - sub.created_utc > 54000 or sub.score < 750):
			if sub.id in cache:
				continue
			else:
				cache.append(sub.id)
				hour_diff = int( (the_time-sub.created_utc)/3600 )
				s.notify(text = sub.title + "\nThere's an open position on /r/Futurology! The top post has *" + str(sub.score) + " points* and was posted *" + str( hour_diff ) + " hours* ago.")
				# print "There's an open position on /r/Futurology! The top post has *" + str(sub.score) + " points* and was posted *" + str( hour_diff ) + " hours* ago."

while True:
	run_bot()
	s.notify(text = "sleeping....")
	# print "sleeping..."
	time.sleep(30) # 30 minutes call interval