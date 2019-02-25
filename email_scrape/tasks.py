import requests
import re
import csv
import urllib3
import time
import os

from bs4 import BeautifulSoup
from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings
import instaloader
import pandas as pd
from .models import ScrapeRequest

urllib3.disable_warnings()

except_strings = ['.png', 'jpg']


@shared_task
def scrape(s_id):
    scrape_request = ScrapeRequest.objects.get(id=s_id)
    result_path = 'csv/result/'
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    result_csv_path = result_path + time.strftime("%Y_%m_%d_%H_%M_%S_") + '.csv'

    in_loader = instaloader.Instaloader()

    with open(scrape_request.csv_path, encoding='utf-8') as csv_file:
        with open(result_csv_path, 'w') as output_file:
            reader = csv.reader(csv_file)
            # writer = csv.writer(output_file, delimiter=",", lineterminator="\n")
            # writer.writerow(['website', 'facebook', 'instagram', 'email'])
            # i = 0
            t_no = 1
            for tag in reader:
                success = True
                df = pd.DataFrame(columns=['name'])
                print("No ", t_no, " : #", tag, )
                users = set()
                c = 0
                u = 0
                try:

                    for post in in_loader.get_hashtag_posts(tag):
                        try:
                            c = c + 1
                            # print("#", tag, "tag's post_No:", c)
                            if post.owner_username not in users:
                                u = u + 1
                                users.add(post.owner_username)
                                df = df.append({'name': post.owner_username}, ignore_index=True)
                                df.to_csv(f'{tag}.csv', header=False, index=False)
                        except Exception as e:
                            print('exception: ', e)
                            if post.owner_username not in users:
                                df = df.append({'name': post.owner_username}, ignore_index=True)
                                df.to_csv(f'{tag}.csv', header=False, index=False)
                                success = False
                except Exception as e:
                    with open(f'{tag}except.txt', mode='w') as f:
                        f.write(str(e))
                        success = False
                df.to_excel(f'{tag}.xlsx', header=False, index=False)
                print("-------#", tag, " : completed, success: ", success)
                print(tag, "tag's post_all_count:", c)
                print(tag, "tag's post_unique_count:", u)
                t_no = t_no + 1

            scrape_request.result_csv_path = result_csv_path
            scrape_request.status = 1
            scrape_request.save()

    message = EmailMessage("Scraped Result", "Here is the scraped result: {}.".format(scrape_request.subject), settings.DEFAULT_FROM_EMAIL,
                           [scrape_request.email])
    message.attach('{}.csv'.format(scrape_request.subject), open(result_csv_path).read(), 'text/csv')
    f = message.send()
    return f