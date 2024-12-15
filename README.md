# Purpose
When disecting individual components from a complex ML application, it is crucial to ensure functional accuracy.
This API is a simple decorator that allows you to record data passed into and returned from the function you plan to dissect, to generate test cases that reflect the actual behavior of the function in the ML application in real scenarios.
# Usage
Specify `--mlsnapshot` command line argument with the path to the folder you would like to save your test cases (if not specified, nothing will be recorded)