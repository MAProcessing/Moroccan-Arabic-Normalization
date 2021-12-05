"""
Created on Wed Feb 14 12:47:44 2020

@author: 
"""

CLIENT_SECRETS_FILE = "code_secret_client.json"
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

import os
import pickle
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import codecs
import csv
    
def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
     #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
         # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
             	flow = InstalledAppFlow.from_client_secrets_file(
                 CLIENT_SECRETS_FILE, SCOPES)
             	credentials = flow.run_console()
    
         # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()
    
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
    
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break
    
    return comments

def get_videos(service, **kwargs):
    final_results = []
    results = service.search().list(**kwargs).execute()
    
    i = 0
    max_pages = 3
    while results and i < max_pages:
        final_results.extend(results['items'])
    
        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.search().list(**kwargs).execute()
            i += 1
        else:
            break
    
    return final_results
    
# def search_videos_by_keyword(service, **kwargs):
#     results = get_videos(service, **kwargs)
#     for item in results:
#         print('%s - %s' % (item['snippet']['title'], item['id']['videoId']))
    
#     # keyword = input('Enter a keyword: ')
#     # search_videos_by_keyword(service, q=keyword, part='id,snippet', eventType='completed', type='video')\n"

# def search_videos_by_keyword(service, **kwargs):
#     results = get_videos(service, **kwargs)
#     for item in results:
#         title = item['snippet']['title']
#         video_id = item['id']['videoId']
#         comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
  
    
    # def write_to_csv(comments):
    #     with open('comments.csv', 'w') as comments_file:
    #         comments_writer = csv.writer(comments_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    #         comments_writer.writerow(['Video ID', 'Title', 'Comment'])
    #         for row in comments:
    #             comments_writer.writerow(list(row))
        

def write_to_csv(comments):
    with codecs.open('comments.csv', 'a','utf-8') as comments_file:
        comments_writer = csv.writer(comments_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        comments_writer.writerow(['Video ID', 'Title', 'Comment'])
        for row in comments:
            comments_writer.writerow(list(row))


def search_videos_by_keyword(service, **kwargs):
    results = get_videos(service, **kwargs)
    final_result = []
    #     with open('comments1.csv', 'w') as comments_file:
    #         comments_writer = csv.writer(comments_file, delimiter=',', quotechar='\"', quoting=csv.QUOTE_MINIMAL)
    #         comments_writer.writerow(['Video ID', 'Title', 'Comment'])
    for item in results:
        title = item['snippet']['title']
        video_id = item['id']['videoId']
        comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
        # make a tuple consisting of the video id, title, comment and add the result to 
        # the final list
        final_result.extend([(video_id, title, comment) for comment in comments]) 
    #             i=0
    #             for row in comments:
    #                 comments_writer.writerow(list(row))
    #                 if i==300:
    #                     break
    #                 i+=1
        #break    
    write_to_csv(final_result)

#Get the authorization code
if __name__ == '__main__':
# When running locally, disable OAuthlib's HTTPs verification. When
# running in production *do not* leave this option enabled.
    #os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    #Extract comments
    keyword = input('Enter a keyword: ')
    search_videos_by_keyword(service, q=keyword, part='id,snippet', type='video')


# x=0
# with codecs.open('comments_covid.csv' ,'r','utf-8') as f:
#     while f.readline():
# 	    x+=1
# x