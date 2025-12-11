.. _`Troubleshooting`:

Troubleshooting
===============
This section describes some common issues that can arise and possible solutions.

Issue #1
--------
When trying to push, you can get a "current branch has no upstream branch" error.
To fix this, set the upstream branch by issuing:
.. code-block:: text
$ git push --set-upstream origin <branch-name>

Issue #2
--------
There were several times where I wasn't able to conenct to my Database. Turns out, in order to connect to a database, you must make sure that the docker container holding it is running!
docker compose up -d (in whatever directory your docker-compose.yml is in) will start the container in detached mode.

Issue #3
--------
Making sure that unwanted files are not uploaded to the repository is very important. (may have almost uploaded my .env a couple times)
Make sure to set up a .gitignore file in the root directory of your repository to avoid this issue.