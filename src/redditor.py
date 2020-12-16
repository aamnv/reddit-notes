import os
import praw


class Redditor:

	def __init__(self):
		self.reddit_bot = praw.Reddit(
			client_id=os.environ.get('REDDIT_ID', None),
			client_secret=os.environ.get('REDDIT_SECRET', None),
        	password=os.environ.get('REDDIT_PASS', None),
        	user_agent=os.environ.get('REDDIT_USERAGENT', None),
        	username=os.environ.get('REDDIT_NAME', None)
        )

		self.subreddit_name = os.environ.get('REDDIT_SUBREDDIT', None)


	def post_submission(self, title, text):
		self.reddit_bot.subreddit(self.subreddit_name).submit(title, selftext=text)

		return 200


	def read_submission(self, id):
		submission = self.reddit_bot.submission(id=id)
		submission_text = submission.selftext

		return submission_text


	def list_submissions(self):
		submission_list = []

		for submission in self.reddit_bot.subreddit(self.subreddit_name).new():
			data_dict = {
				'title': submission.title,
				'url': submission.url,
				'id': submission.id
			}

			submission_list.append(data_dict)

		return submission_list


	def delete_submission(self):
		return None