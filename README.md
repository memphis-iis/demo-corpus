demo-corpus
============================

This is a sample web service written in Python using the Flask framework. It's
purpose is to provide a small demonstration of writing a web service for Elastic
Beanstalk on Amazon Web Services.

Note that all of the information below is in our overview video for this project.

Things you should already know
-------------------------------

You should know:

 * How to write a program in Python
 * At least a little something about the Flask framework
 * A little knowledge ReST and web services

If you want to experiment with the web service via the demo web page, you should
also know HTML, CSS, and JavaScript. You should also know the CSS/layout framework
Bootstrap, and the JavaScript library jQuery. This might sound like quite a bit,
but knowing these five things (HTML, CSS, JavaScript, Bootstrap, and jQuery) gives
you enough to easily produce a modern web page.

Requirements
-------------------

At a high level, we require very little:

 * Python 3
 * virtualenv installed for Python 3
 * Flask and it's requirements
 * An AWS account able to deploy to Elastic Beanstalk

Python 3 was chosen because it is currently the default Python version used by
Elastic Beanstalk, so the application is less complicated. If you are using a
Linux-based system, then your package manager's version of Python 3 should be
fine. If you are using Windows or Mac OSX, you might want to consider a "full"
Python distribution that has been pre-built for you. The most popular and general
purpose is ActiveState. You'll want to install virtualenv and pip - please see
[https://code.activestate.com/pypm/virtualenv/](https://code.activestate.com/pypm/virtualenv/).

Perhaps the most popular "scientific" Python distribution is Anaconda; this is an
excellent choice if you plan on using python packages like scipy or pandas. However,
you will also need to read the `conda env` documentation since it is slightly
different from the standard python tool `virtualenv`. Once you have an environment
setup, you can use `pip` and the `requirements.txt` as below.

Setting up for development
------------------------------

We **strongly** recomend using a virtualenv for development. There are many benefits
to using a virtual Python environment. In this case, perhaps the greatest benefit
is that you'll be able to more accurately model the Elastic Beanstalk environment
when you are running the application on your local workstation.

Setting up is handled for you in the shell script `setup.sh`.


Sample AWS web service written in Python

Notes:

- AWS EB will use Python3

- For Flask under Python 3, we need to make sure we're using the latest
  versions of itsdangerous, Jinja2 and Werkzeug

- We need a requirements.txt file

- The main file should be application.py

- Our WSGI application should be named application - in our case we
  alias our object named `app`
