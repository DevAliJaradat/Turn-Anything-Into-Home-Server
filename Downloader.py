# parse config file
server_config = [line.strip().split('=') for line in open('server_conf.txt').readlines() if line[0]!='#' and line!='']
config = {e[0]:e[1] for e in server_config}

def download_video_function(url):
    # import libs 
    from pytubefix import YouTube
    from pytubefix.cli import on_progress
    from pytube.innertube import _default_clients
    _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

    yt = YouTube(url, on_progress_callback=on_progress)
    ys = yt.streams.get_highest_resolution()
    ys.download(config['MEDIA_DIR'])

def download_audio_function(url):
    from pytubefix import YouTube
    from pytubefix.cli import on_progress
    from pytube.innertube import _default_clients
    _default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


    yt = YouTube(url, on_progress_callback=on_progress)
    ys = yt.streams.get_audio_only()
    print(ys.title)
    ys.download(config['MEDIA_DIR'],f'{ys.title}.mp3')

