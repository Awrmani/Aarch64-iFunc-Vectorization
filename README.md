# Aarch64 iFunc Vectorization

The created tool is called ifuncCreater.py.

This program can takes as many function files as needed!

The existance of resolver.txt in the same folder is essential for this program.

## Files

ifuncCreator is the created tool to make the required functions and use iFunc to determine between the function implementations and choose the right one based on the system compatibility.

function.c - is the initial sample function file which will be used for testing.

function.h - includes the prototype of the function.c which in this sample is called adjust_channels.

resolver.txt - includes the template for the iFunc function with the matching resolver argument name.

function_altered.c - is the new file created after running ifuncCreator.py.

## Run Command

./ifuncCreator function.c adjuster.c ... compile


or for no main compilation:

./ifuncCreator function.c adjuster.c ...
