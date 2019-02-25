import signal
import os
import sys
# from datetime import datetime
# from itertools import dropwhile, takewhile
try:
    import instaloader
    import pandas as pd
except:
    os.system('pip install -r requirements.txt')
    print('installing packages please reload')

l = instaloader.Instaloader()



def signal_handler(*args):
    print("received signal\n")
    df.to_excel(f'{tag}.xlsx', header=False, index=False)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
tags = input(r'enter your hashtag list (without #, e.g: aaa bbb ccc): ')
tags = tags.strip().split(" ")
print('running')
print("tag list", tags)
# SINCE = datetime(2018, 9, 30)
# UNTIL = datetime(2019, 12, 1)
t_no = 1
for tag in tags:
    success = True
    df = pd.DataFrame(columns=['name'])
    print("No ", t_no, " : #", tag,)
    users = set()
    c = 0
    u = 0
    try:
        # posts = l.get_hashtag_posts(tag)
        # for post in takewhile(lambda p: p.date > UNTIL, dropwhile(lambda p: p.date > SINCE, posts)):

        for post in l.get_hashtag_posts(tag):
            try:
                c = c + 1
                # print("#", tag, "tag's post_No:", c)
                if post.owner_username not in users:
                    u = u + 1
                    users.add(post.owner_username)
                    df = df.append({'name':post.owner_username}, ignore_index=True)
                    df.to_csv(f'{tag}.csv',header=False,index=False)
            except Exception as e:
                print('exception: ', e)
                if post.owner_username not in users:
                    df = df.append({'name':post.owner_username}, ignore_index=True)
                    df.to_csv(f'{tag}.csv',header=False,index=False)
                    success = False
    except Exception as e:
        with open(f'{tag}except.txt', mode = 'w') as f:
            f.write(str(e))
            success = False
    df.to_excel(f'{tag}.xlsx', header=False, index=False)
    print("-------#", tag,  " : completed, success: ", success)
    print(tag, "tag's post_all_count:", c)
    print(tag, "tag's post_unique_count:", u)

    t_no = t_no + 1

