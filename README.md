demo-corpus
============================

This is a sample web service written in Python using the Flask framework. It's
purpose is to provide a small demonstration of writing a web service for
Elastic Beanstalk on Amazon Web Services.

Note that all of the information below is in our overview video for this
project.


Things you should already know
-------------------------------

You should know:

 * How to write a program in Python
 * At least a little something about the Flask framework
 * A little knowledge ReST and web services

If you want to experiment with the web service via the demo web page, you
should also know HTML, CSS, and JavaScript. You should also know the
CSS/layout framework Bootstrap, and the JavaScript library jQuery. This might
sound like quite a bit, but knowing these five things (HTML, CSS, JavaScript,
Bootstrap, and jQuery) gives you enough to easily produce a modern web page.


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
Python distribution that has been pre-built for you. The most popular and
general purpose is ActiveState. You'll want to install virtualenv and pip -
please see
[https://code.activestate.com/pypm/virtualenv/](https://code.activestate.com/pypm/virtualenv/).

Perhaps the most popular "scientific" Python distribution is Anaconda; this is
an excellent choice if you plan on using python packages like scipy or pandas.
However, you will also need to read the `conda env` documentation since it is
slightly different from the standard python tool `virtualenv`. Once you have
an environment setup, you can use `pip` and the `requirements.txt` as below.


Setting up for development
------------------------------

We **strongly** recomend using a virtualenv for development. There are many
benefits to using a virtual Python environment. In this case, perhaps the
greatest benefit is that you'll be able to more accurately model the Elastic
Beanstalk environment when you are running the application on your local
workstation.

Setting up is handled for you in the shell script `setup.sh` (or `setup.bat`
if you are running on Windows). Note that if you are using the Anaconda Python
distribution you'll need to set up a conda env on your own.

You'll also need to install and start up a local DynamoDB instance.To setup
"DynamoDB Local" you can just follow the directions at
[http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html](http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html)

The instructions mainly boil down to:

  * Download the .zip or .tar.gz archive
  * Extract everything somewhere appropriate.Below this directory will be
    referred to as the "DynamoDB directory"
  * Run the server whenever you are testing. 

That last step is the doozy: if you aren't running the local DynamoDB server,
the web application will have errors when your are running in on your local
workstation. You can still write code, execute the unit tests, push your
changes to a repository, etc, but you won't be able to actually run the
entire web application if you aren't running DynamoDB Local.

Unfortunately there isn't a simple script file (BAT file for Windows people) in
the distributed files for running the server. You can create your own and just
add the line:
`java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar`.
Then when you want to run the server, you can open your terminal (command
prompt for Windows people), `cd` to your DynamoDB directory, and run
your script file.

You might also want to download a tool like the SQLite Browser available at
http://sqlitebrowser.org/. DynamoDB Local uses SQLite to store data, so while
you are testing you can just use this handy browser to view the data in the
database file in your DynamoDB directory (hint: the database file name will
end in `.db`)


Some Elastic Beanstalk Notes
--------------------------------------

 * We default to Python 3 because that's what Elastic Beanstalk currently uses.

 * By default, Elastic Beanstalk expects a file named application.py and the Flask
   instance inside that file to be named application.

Neither of these two issues are written in stone, but if you want different
behavior, then you should look into using EB configuration files. At the time
of this writing, you could find the documentation
[here](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-custom-container.html)

Essentially, you would create a configuration file in the `.ebextensions`
directory of your project and include it in the application bundle that you
upload. The configuration file name should end with `.config` and be in either
YAML or JSON format. Note that you can have as many configuration files as you
like as long as they are formatted correctly, named correctly, and placed in
the correct locations
