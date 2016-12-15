import tweepy

class APIWrapper(object):
	"""
	Defines a wrapper for the Tweepy API that ables to simplify the auth process and data obtention

	@param  _auth   authentication object
	@param  _api	real Tweepy API object
	"""
	__slots__ = ["_auth","_api"]

	def __init__(self):
		"""
		Initializes an empty wrapper
		"""
		self.authenticate("","","","")
	@classmethod
	def withAuthentication(cls,consumerKey,consumerSecret,accessToken,accessSecret):
		"""
		Initializes and authenticates a new API wrapper object

		@see	authenticate
		@return	 already authenticated API object
		"""
		obj = cls()
		obj.authenticate(consumerKey,consumerSecret,accessToken,accessSecret)
		return obj

	def authenticate(self,consumerKey,consumerSecret,accessToken,accessSecret):
		"""
		Authenticates the API wrapper using the Twitter app's data
		All data can be retrieved by creating a Twitter application from this URL:
		https://apps.twitter.com
		All data auth have to be strings
		"""
		self._auth = tweepy.OAuthHandler(consumerKey,consumerSecret)
		self._auth.set_access_token(accessToken,accessSecret)
		self._api = tweepy.API(self._auth)

	def getUserTweets(self,user):
		"""
		Given a user, retrieves its status and returns an iterator that can loop through them

		@param 		user 	id/nickname of the user
		@return 	iterator to loop between retrieved status
		"""
		return tweepy.Cursor(self._api.user_timeline, id=user)

	@property
	def api(self):
		"""
		Returns the Tweepy API object
		"""
		return self._api

	@property
	def auth(self):
		"""
		Returns the Tweepy auth object
		"""
		return self._auth
