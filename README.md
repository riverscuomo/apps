# apps
My monorepo of python scripts, modules, and packages. I'm currently publishing this only to get help with some issues. Almost all of the files are gitignored. https://github.com/riverscuomo/apps/blob/master/.gitignore


Please let me know if this doesn't seem like a reasonable way to import and run a large number of packages on a regular schedule.

here is the report it prints after running each day.


![image](https://user-images.githubusercontent.com/24362267/218493412-d48bccbd-54e4-462a-987d-bd23849c1b3e.png)

## Installation
### Create the venv (use the name of the computer, such as G for desktop or 9 for laptop)
"C:\Users\aethe\AppData\Local\Programs\Python\Python310\python" -m venv .G
"C:\Users\Rivers Cuomo\AppData\Local\Programs\Python\Python310\python.exe" -m venv .9

Make sure you open a new terminal to activate the venv. Otherwise you'll be installing packages into the global python environment?

### Install the packages in requirements.txt into the venv\Lib\site-packages directory
`pip install -r requirements.txt`

You'll notice the local packages are not installed. That's because they are not in the requirements.txt file. You need to install them separately.

`cd gspreader`
`pip install -e .`

<!-- pip install -e crawlers/lastfmcrawler/.
pip install -e crawlers/spotifycrawler/. -->
pip install -e crawlers/.
pip install -e demos/.
pip install -e kyoko/.
pip install -e new_albums/.
pip install -e social/.
pip install -e spotnik/.

These are published on pypi, so you technically could put them in requirements.txt, but I don't want to do that because I want to be able to edit them locally and have the changes take effect immediately?
pip install -e gspreader/.
pip install -e rivertils/.



## Notes
To install the submodules in a way that you'll always have the latest commit, try this in each submodule directory:
"If you do what's called an editable install you won't have to re-install your own code that you're actively editing. People typically do that with `pip install -e .` You can then point pip at the directory holding the code, e.g. . is common for the current directory."

`pip install -e .` = "Install the project found in the current directory".

Editable installs allow you to install your project without copying any files. Instead, the files in the development directory are added to Python’s import path. This approach is well suited for development and is also known as a “development installation”.

So if I ran `pip install -e .` on apps/, it wouldn't install all the projects in apps/ as packages. You need to install each project separately by navigating to their directory and running `pip install -e .` in each one. All you need to do in apps/ is run `pip install -r requirements.txt` to install all the packages in the requirements.txt file.

## Daily Runs From the `Maintenance.py` Script:
I think maintenance.py is importing and running the (editable) installed version in .venv\Lib\site-packages\

