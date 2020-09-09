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
# if enabled, show verbose messages
verbose_error = 1

while True:
    try:
        spinner.start()
        subreddit = reddit.subreddit('random')
        domains = ['i.redd.it', 'i.imgur.com']
        limit = None
        # begin boot info
        spinner.info('KarmaBot by Mr-Steal-Your-Script, modified by SoulRepo')
        spinner.info('NOTE: Using this on your main account will likely get you suspended. Use an alt before you try this out.')
        spinner.info('Subject of bot is: ', config.UN)
        spinner.info('Latest updates can be found at https://github.com/SoulRepo/KarmaBot')
        # show targeted subreddit
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
            spinner.info('Domain ', submission.domain, 'is not in the text database, writing it to domains.txt')
            with open ('domains.txt', "a") as domain:
                domain.write(submission.domain + "\n")
    if verbose_error == 1
        except Exception as e:
            exc = str(str(e))
            spinner.fail(text=exc)
            spinner.info('Pausing for ', sleep_timer, 'seconds. To modify timer, change sleep_timer variable in main.py.')
            time.sleep(sleep_timer)
    else
        spinner.fail('Failure to post, pausing for ', sleep_timer, 'seconds. Timer can be modified in main.py.')
        spinner.info('To check full details, enable verbose errors.')
        time.sleep(sleep_timer)
    
    except KeyboardInterrupt:
        spinner.warn(text='Shutting down bot.')
        quit()
