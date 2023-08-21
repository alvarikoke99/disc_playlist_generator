import os, sys, shutil

formats = (".chd", ".iso", ".cso", ".rvz")

symbol = ")"

def obtain_pattern(filename, symbol = symbol): 
    try:
        return filename[0:filename.index(symbol)+1].rstrip()
    except:
        return filename[0:filename.index('.')].rstrip()

def create_folder(dir_name, files):
    dir = os.path.join(".", dir_name)
    try:
        os.mkdir(dir)
        print("Created folder: " + dir_name)
        playlist = open(os.path.join(dir, dir_name), "w")
        for file in files:
            shutil.move(os.path.join(".", file), os.path.join(dir, file))
            playlist.write(file + "\n")
            print(file)
        playlist.close()
        print("---------------------------")
    except Exception as e:
        print("Error creating folder")
        print(e)

current_files = []
current_playlist = ""
files = os.listdir()
dir_size = len(files)

print("===========================")
print("M3U DISC PLAYLIST GENERATOR")
print("===========================")

if(len(sys.argv) == 2):
    try:
        symbol = sys.argv[1]
    except:
        print("Error parsing command line argument")

print("Using symbol: " + symbol)
print("---------------------------")

for i in range(dir_size+1):
    if (i == dir_size):
        if(len(current_files) > 1):
            create_folder(current_playlist + ".m3u", current_files)

    elif(files[i].endswith(formats)):
        file = files[i]
        if(i == 0):
            current_playlist = obtain_pattern(file)
            current_files.append(file)
        elif(obtain_pattern(file) == current_playlist):
            current_files.append(file)
        else:
            if(len(current_files) > 1):
                create_folder(current_playlist + ".m3u", current_files)
            current_playlist = obtain_pattern(file)
            current_files = [file]
