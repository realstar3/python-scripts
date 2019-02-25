YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'
def get_video_comment(self):

    def load_comments(self):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            print("Comment by {}: {}".format(author, text))
            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    rauthor = reply['snippet']['authorDisplayName']
                    rtext = reply["snippet"]["textDisplay"]

                print("\n\tReply by {}: {}".format(rauthor, rtext), "\n")

    parser = argparse.ArgumentParser()
    mxRes = 20
    vid = str()
    parser.add_argument("--c", help="calls comment function by keyword function", action='store_true')
    parser.add_argument("--max", help="number of comments to return")
    parser.add_argument("--videourl", help="Required URL for which comments to return")
    parser.add_argument("--key", help="Required API key")

    args = parser.parse_args()

    if not args.max:
        args.max = mxRes

    if not args.videourl:
        exit("Please specify video URL using the --videourl=parameter.")

    if not args.key:
        exit("Please specify API key using the --key=parameter.")

    try:
        video_id = urlparse(str(args.videourl))
        q = parse_qs(video_id.query)
        vid = q["v"][0]

    except:
        print("Invalid YouTube URL")

    parms = {
                'part': 'snippet,replies',
                'maxResults': args.max,
                'videoId': vid,
                'key': args.key
            }

    try:

        matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
        i = 2
        mat = json.loads(matches)
        nextPageToken = mat.get("nextPageToken")
        print("\nPage : 1")
        print("------------------------------------------------------------------")
        load_comments(self)

        while nextPageToken:
            parms.update({'pageToken': nextPageToken})
            matches = self.openURL(YOUTUBE_COMMENT_URL, parms)
            mat = json.loads(matches)
            nextPageToken = mat.get("nextPageToken")
            print("\nPage : ", i)
            print("------------------------------------------------------------------")

            load_comments(self)

            i += 1
    except KeyboardInterrupt:
        print("User Aborted the Operation")

    except:
        print("Cannot Open URL or Fetch comments at a moment")