import sys
try:
    file = sys.argv[1]
except:
    print("Give the name of the study file to run!")
    sys.exit()
print("Starting:", file, end='\n\n')

if file == 'map':
    from study import map
elif file == 'arch':
    from study import architecture_state_machine
else:
    print("Check study.py to see the options...")