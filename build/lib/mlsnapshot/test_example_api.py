from api import MLSnapshot
stuff = MLSnapshot.retrieve('run_nov/snapshots','example_function')
args,kwargs,output1=stuff[0]
print(args)
print(kwargs)
print(output1)