# apps
My monorepo of python scripts, modules, and packages. I'm currently publishing this only to get help with some issues. Almost all of the files are gitignored.

## Current Issue: How to run the packages from another script

I have a python script `apps\maintenance.py` that imports a number of my packages and runs them. As I've converted some of these packages to poetry, I can't figure out how to get them to run. They're importing just fine but then I get this error when I call main() on the import.

maintenance.py is a master script that imports and runs many other Scripts, some daily some weekly. It's triggered by Windows task scheduler every night. Some of the scripts are simple modules that sit in the same directory, such as pool.py, and others are packages that sit in the same directory, such as "New Albums" and "Spotnik". (A full list of the Imports can be found in maintenance_config.py.) I want all of these scripts and packages to be runnable by anyone on the command line and also programmatically by the maintenance.py script. So far, through our efforts in this GitHub issue, it looks like the simple modules, such as pool.py are working well, and a number of the packages are working well, such as "New Albums", "Social", and "Spotnik".

Next up I'd like to tackle "crawlers", which right now is a directory within apps which has three packages in it, spotifycrawler, LastFMcrawler and a package of common code called core. I'd like maintenance.py to be able to import and run spotifycrawler and LastFMcrawler.

Please let me know if this doesn't seem like a reasonable way to import and run a large number of packages on a regular schedule.


![image](https://user-images.githubusercontent.com/24362267/218493412-d48bccbd-54e4-462a-987d-bd23849c1b3e.png)

