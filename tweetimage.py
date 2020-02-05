import tweepy
import os
import io
import urllib.request
from google.cloud import vision
from google.cloud.vision import types

consumer_key = 'sdaw'
consumer_secret = 'wqer'
access_key = 'acxc'
access_secret = 'saqwe'

def get_all_tweets(account):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []
        new_tweets = api.user_timeline(screen_name = account,count=1)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1
        tweetnum = 1
        while(tweetnum < 10):
                new_tweets = api.user_timeline(screen_name = account, count=1, max_id = oldest)
                alltweets.extend(new_tweets)
                tweetnum += 1
                oldest = alltweets[-1].id - 1

        outtweets = []
        fileorder = 1
        for tweet in alltweets:
                try:
                        url = str(tweet.entities['media'][0]['media_url'])
                        name = 'C:/Users/Vanquish/Desktop/pyve/VisionApi/downloadimage/' + str(fileorder) + '.jpg'
                        urllib.request.urlretrieve(url,name)
                        fileorder += 1
                except (NameError, KeyError):

                        pass
                else:

                        outtweets.append([tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.entities['media'][0]['media_url']])
        return fileorder
def googlevision(f):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'TweetImage-ef41c01d2f34.json'
        client = vision.ImageAnnotatorClient()
        path = r'C:\Users\Vanquish\Desktop\pyve\VisionApi\downloadimage'
        file_name = 1
        while(file_name < f):
                with io.open(os.path.join(path, str(file_name) + '.jpg'),'rb') as image_file:
                        content = image_file.read()
                image = vision.types.Image(content = content)
                response = client.text_detection(image = image)
                texts = response.text_annotations
                print('Texts of Image' + str(file_name) + ':')
                for text in texts:
                        print('\n"{}"'.format(text.description))

                if response.error.message:
                        raise Exception(
                                '{}\nFor more info on error messages, check: '
                                'https://cloud.google.com/apis/design/errors'.format(
                                response.error.message))
                response = client.image_properties(image=image)
                props = response.image_properties_annotation
                print('Properties of image' + str(file_name) + ':')

                for color in props.dominant_colors.colors:
                        print('fraction: {}'.format(color.pixel_fraction))
                        print('\tr: {}'.format(color.color.red))
                        print('\tg: {}'.format(color.color.green))
                        print('\tb: {}'.format(color.color.blue))
                        print('\ta: {}'.format(color.color.alpha))

                if response.error.message:
                        raise Exception(
                                '{}\nFor more info on error messages, check: '
                                'https://cloud.google.com/apis/design/errors'.format(
                                response.error.message))
                file_name += 1
if __name__ == '__main__':
        f = get_all_tweets('@realDonaldTrump')
        googlevision(f) 
