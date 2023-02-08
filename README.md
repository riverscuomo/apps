# apps
My monorepo of python scripts, modules, and packages. I'm currently publishing this only to get help with some issues. Almost all of the files are gitignored.

## Current Issue: How to run a package from another script

I have a python script that imports a number of my packages and runs them. As I've converted some of these packages to poetry, I can't figure out how to get them to run. They're importing just fine but then I get this error when I call main() on the import.

Here's the script that imports and attempts to run my package:
