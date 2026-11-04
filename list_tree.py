import os
for root, dirs, files in os.walk('src/numu_tech'):
    dirs[:] = [d for d in dirs if d != '__pycache__']
    print(root)
    for f in sorted(files):
        print('  ' + f)