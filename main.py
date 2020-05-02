import asyncio
from pyppeteer import launch
import sys
import time
import os, getopt, getpass

async def main(username, videoUrl, timeout, no_check_certificate):
    
    passw = getpass.getpass()
    
    browser = await launch({'headless':False, 'timeout':timeout})
    page = await browser.newPage()

    try:
        await page.goto(videoUrl, { 'waitUntil':'networkidle2' })
    except Exception as ex:
        print(ex)
        print('If a navigation timeout occurs, try adding more than 30 seconds as timeout with the --timeout=seconds option (this may be due to slow internet connection or overloaded computer and Chromium)')
        exit()
    
    await page.waitForSelector('input[type="email"]')
    print("Typing username...")
    await page.keyboard.type(username)
    await page.click('input[type="submit"]')
    time.sleep(2)
    await page.waitForSelector('input[type="password"]')
    await page.keyboard.type(passw)
    await page.click('input[type="submit"]')
    time.sleep(2)
    await page.waitForSelector('input[type="button"]')
    await page.click('input[type="button"]')
    time.sleep(10) #Tomémonos un tiempo for da cookies to generate dawg
    cookie = await page.cookies('https://.api.microsoftstream.com') 
    mpdTimeManifestUrl = await page.evaluate('amp.Player.players["vjs_video_3"].cache_.src')
    print(mpdTimeManifestUrl)
    m3u8ManifestUrl = mpdTimeManifestUrl[:mpdTimeManifestUrl.rfind('/')] + '/manifest(format=m3u8-aapl)'
    print(m3u8ManifestUrl)
    ytDlCookies = ''
    for i in cookie:
        if i['name'] == 'Authorization_Api' or i['name'] == 'Signature_Api':
            ytDlCookies += f"{i['name'][:-4]}={i['value']}; "

    video_title = await page.evaluate('document.title')
    video_title = video_title.replace(" ", "_")
    print(ytDlCookies)
    #await browser.close()
    ytDlCommand = f"youtube-dl {no_check_certificate} --output '{video_title}.mp4' --no-call-home --add-header \"Cookie:{ytDlCookies}\" \"{m3u8ManifestUrl}\""
    print("")
    print(ytDlCommand)
    os.system(ytDlCommand)

options = getopt.getopt(sys.argv[1:],'',['username=', 'video=', 'no-check-certificate'])
username_arg = None
video_arg = None
no_check_certificate_arg = ''
errs = False
timeout_arg = 30000

for opt, arg in options[0]:
    if opt in ('--username'):
        username_arg = arg
    if opt in ('--video'):
        video_arg = arg
    if opt in ('--timeout'):
        if not isinstance(arg, int):
            print('The --timeout option requires an integer argument, for example to set 30 seconds as timeout pass --timeout=30\n')
            errs = True
        else:
            timeout_arg = arg * 1000 #the argument should be in milliseconds but I hate time arguments in milliseconds so yeah, here you are

if opt in ('--no-check-certificate'):
    no_check_certificate_arg = '--no-check-certificate'

if username_arg is None:
    print('--username parameter is missing, pass your MS Stream account username with --username=myusername@email.com\n')
    errs = True
if video_arg is None:
    print('--video parameter is missing, pass the video link with --video=link\n')
    errs = True

if not errs:
    asyncio.get_event_loop().run_until_complete(main(username_arg, video_arg, timeout_arg, no_check_certificate_arg))