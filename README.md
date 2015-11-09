Faffy Video Downloader README.md

This project is focused on creating a flexable CLI based YouTube video/audio downloader.

usage: Faffy.py [-h] [-u URL] [-a] [-l LIMIT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Youtube URL to download video from. Passing this
                        argument will cause the program to exit the the
                        terminal when the task is completed
  -a, --audio-only      Optional flag, that causes the downloader to save only
                        the audio track of a video.
  -l LIMIT, --limit LIMIT
                        If --url is a playlist, this chooses the starting
                        point, and the ending point for the downloader. list
                        starts at 0, and -1 is always the very last video.
                        default: 0:-1 format : start:end

