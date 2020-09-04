import time
import praw
import random
import config
import pyimgur
from halo import Halo

spinner = Halo(spinner={'interval': 100, 'frames': ['-', '+', '*', '+', '-']})

reddit = praw.Reddit(client_id=config.C_ID, client_secret=config.C_S, user_agent=config.U_A, username=config.UN, password=config.PW)
imgur_id = config.I_ID

#how long it waits per each error
sleep_timer = 30

while True:
    try:
        spinner.start()
        subreddit = reddit.subreddit('random')
        domains = ['i.redd.it', 'i.imgur.com']
        limit = None
        spinner.info('KarmaBot by Mr-Steal-Your-Script, modified by SoulRepo')
        print('Targeted subreddit is: ', subreddit)
        
        submissions = list(subreddit.top('all', limit=limit))
        submission = random.choice(submissions)
        if submission.domain in domains:
            im = pyimgur.Imgur(imgur_id)
            uploaded_image = im.upload_image(url=submission.url)
            with open ('links.txt', "a") as f:
                f.write(uploaded_image.link + "\n")
            reddit.validate_on_submit = True
            subreddit.submit(submission.title, url=uploaded_image.link)
            spinner.succeed('Success, posted to reddit with id', submission.id)
            
        elif submission.domain not in domains:
            spinner.info('domain ' submission.domain 'is not in the text database, writing it to domains.txt')
            with open ('domains.txt', "a") as domain:
                domain.write(submission.domain + "\n")
    except Exception as e:
        exc = str(str(e))
        spinner.fail(text=exc)
        spinner.info('Pausing for ', sleep_timer, 'seconds. To modify timer, change sleep_timer variable in python file.')
        time.sleep(sleep_timer)
        
    except KeyboardInterrupt:
        spinner.warn(text='Shutting down bot. Come bot soon! ;)')
        quit()
