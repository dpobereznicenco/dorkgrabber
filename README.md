# dorkgrabber
A google dork grabber.

This tool does not bypass the captcha but grabs the link from google and you only care of providing the captcha when it's asked.

How to use:

python dorkgrabber.py dork
python dorkgrabber.py site:.mywebsite.com

This will scrape the 1 to 100 page.

python dorkgrabber.py dork start-stop
python dorkgrabber.py site:.mywebsite.com 10-200

This will scrape the 2 to 200 page.


When google ask for captcha you go in the current folder and open image.jpg .


This script works with pycurl.
