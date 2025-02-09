from googleapiclient.discovery import build
import isodate

API_KEY = "AIzaSyCJFZwMAhMgnAM-O9EJySa5rLs4YOUZ2HY"
playlist_id = "PLGjplNEQ1it_oTvuLRNqXfz_v_0pq6unW"

youtube = build("youtube", "v3", developerKey=API_KEY)

def get_playlist_duration(playlist_id):
    total_seconds = 0
    next_page_token = None

    while True:
        playlist_items = youtube.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = [item["contentDetails"]["videoId"] for item in playlist_items["items"]]

        video_details = youtube.videos().list(
            part="contentDetails",
            id=",".join(video_ids)
        ).execute()

        for video in video_details["items"]:
            duration = isodate.parse_duration(video["contentDetails"]["duration"])
            total_seconds += duration.total_seconds()

        next_page_token = playlist_items.get("nextPageToken")
        if not next_page_token:
            break

    hours, remainder = divmod(int(total_seconds), 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours} hours, {minutes} minutes, {seconds} seconds"

print(get_playlist_duration(playlist_id))
