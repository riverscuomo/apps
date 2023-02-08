# apps
My monorepo of python scripts, modules, and packages. I'm currently publishing this only to get help with some issues. Almost all of the files are gitignored.

## Current Issue: How to run the packages from another script

I have a python script `apps\maintenance.py` that imports a number of my packages and runs them. As I've converted some of these packages to poetry, I can't figure out how to get them to run. They're importing just fine but then I get this error when I call main() on the import.


## How to reproduce the error
In the `apps` directory, run `py maintenance.py -m new_albums`. This should run the script with an argument to import and run the `apps\new_albums` package. You should then see some variation of this error:

`module 'new_albums' has no attribute 'main'`

Finally, the `new_albums` package runs fine if change to the `new_albums` package directory and run  `py new_albums`.

Is there something wrong with the way I've set up the `new_albums` package with poetry? I should be able to import and run its `main` function, correct?
