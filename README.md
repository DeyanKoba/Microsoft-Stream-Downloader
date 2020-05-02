# Microsoft-Stream-Downloader
A simple tool to download Microsoft Stream videos based on python, pyppeeteer and youtube-dl

## Requirements
The minimum python version is `3.6`. <br />
Make sure you have installed `youtube-dl` (https://github.com/ytdl-org/youtube-dl) and pyppeteer `python3 -m pip install pyppeteer`

## Why?
In Italy the universities have been closed since February due to COVID-19 and the main tool used to continue with the classes online is Microsoft Teams which automatically saves the lessons on Microsoft Stream.
The main problem is that not everyone has good internet connection or limited traffic plans so saving the videos for offline viewing would be useful for everyone. <br />
This tools is born with this purpose (no I don't think it's theft, the classes can be recorded by anyone and nobody gets hurt if we just download them), it logins into your Microsoft Stream account, downloades the `m3u8-aapl` manifest along with the authorization cookies and passes them to `youtube-dl` that downloads all the fragments and joins them into a single video for multiple offline views.

**NOTE**

This repo is meant to be a tool developed quickly so I could start downloading my classes quickly so it's not perfect. All tips are welcome! 


## How it works
sample usage:
```
python3 main.py --username=emailUsedForMsStream@email.com --video=https://web.microsoftstream.com/video/some-interesting-video-url
```

```
--username=<USERNAME>       The username/email used to login into you MS Stream account (REQUIRED)
--video=<URL>               The url of the video to download (REQUIRED)
--no-check-certificate      Passes the --no-check-certificate option to youtube-dl and avoids checking the SSL certificate
--timeout=<SECONDS>         If Chromium is struggling connecting to Microsoft Stream or closes while loading, try increasing the timeout, by default it's set to 30 seconds
```

---
**NOTE**

Sometimes youtube-dl raises the `CERTIFICATE_VERIFY_FAILED` error, you can use a temporary workaround by passing the extra argument `--no-check-certificate` <br />
For more info and solutions please refer to https://github.com/ytdl-org/youtube-dl/issues/4816
---

