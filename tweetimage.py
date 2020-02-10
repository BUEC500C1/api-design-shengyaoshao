import tweepy
import os
import io
import urllib.request
from google.cloud import vision
from google.cloud.vision import types

consumer_key = 'asdasd'
consumer_secret = 'asdasd'
access_key = 'asdasd'
access_secret = 'asdasd'

def get_all_tweets():
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []
        print("enter the name of the twitter account")
        account = input()
        print("How many tweets you would like to scan, you can scan as many as 200")
        number = input()
        while (int(number) > 200):
                print('The number you entered is biger than 200, please enter a number less than 200')
                number = input()
        try:
                new_tweets = api.user_timeline(screen_name = account,count=1)
        except:
                print('This is not a valid Twitter account')
                get_all_tweets()
        alltweets.extend(new_tweets)
        try:
                oldest = alltweets[-1].id - 1
        except:
                print('This account does not have this many tweets')
                get_all_tweets()
        tweetnum = 1
        while(tweetnum <= int(number)):
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
        imagenum = fileorder - 1
        print(str(imagenum)+'images detected')
        return fileorder
def googlevision(f):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'TweetImage-ef41c01d2f34.json'
        client = vision.ImageAnnotatorClient()
        path = r'C:\Users\Vanquish\Desktop\pyve\VisionApi\downloadimage'
        file_name = 1
        if(f == 1):
                print("No image posted by this account in the recent 10 tweets")
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

                response = client.face_detection(image=image)
                faces = response.face_annotations
                # Names of likelihood from google.cloud.vision.enums
                likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
                print('Faces:')

                for face in faces:
                        if (likelihood_name[face.anger_likelihood] == 'VERY_LIKELY'):
                                print('This person is very likely to be angery')
                        elif (likelihood_name[face.anger_likelihood] == 'LIKELY'):
                                print('This person is likely to be angery')
                        elif (likelihood_name[face.joy_likelihood] == 'VERY_LIKELY'):
                                print('This person is very likely to be happy')
                        elif (likelihood_name[face.joy_likelihood] == 'LIKELY'):
                                print('This person is likely to be happy')
                        elif (likelihood_name[face.surprise_likelihood] == 'VERY_LIKELY'):
                                print('This person is very likely to be surprised')
                        elif (likelihood_name[face.surprise_likelihood] == 'LIKELY'):
                                print('This person is likely to be surprised')
                        else:
                                print('Unable to determine')
                if response.error.message:
                        raise Exception(
                                '{}\nFor more info on error messages, check: '
                                'https://cloud.google.com/apis/design/errors'.format(
                                        response.error.message))
                file_name += 1
if __name__ == '__main__':
        f = get_all_tweets()
        googlevision(f)
