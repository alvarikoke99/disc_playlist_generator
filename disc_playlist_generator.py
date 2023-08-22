import os, sys, shutil

FORMATS = (".chd", ".iso", ".cso", ".rvz")
ADD_EXTENSION = True

symbol = ")"

def obtain_pattern(filename, symbol = symbol): 
    try:
        return filename[0:filename.index(symbol)+1].rstrip()
    except:
        return filename[0:filename.index('.')].rstrip()

def create_playlist(game_name, files):
    playlist_name = game_name + ".m3u"
    if(ADD_EXTENSION):
        dir_name = playlist_name
    else:
        dir_name = game_name
    dir = os.path.join(".", dir_name)
    try:
        #Create folder
        os.mkdir(dir)
        print("Created folder: " + dir_name)
        #Create m3u file
        playlist = open(os.path.join(dir, playlist_name), "w")
        #Add entries
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
files = sorted(os.listdir())
dir_size = len(files)

print("===========================")
print("M3U DISC PLAYLIST GENERATOR")
print("===========================")

#Parse arguments
try:
    arguments = sys.argv[1:]
    while len(arguments) > 0:
        arg = arguments.pop(0)
        if(arg == "-s"):
            symbol = arguments.pop(0)
        elif(arg == "-b"):
            ADD_EXTENSION = False      
except:
    print("Error parsing command line argument")

print("Using symbol: " + symbol)
print("---------------------------")

for i in range(dir_size+1):
    #If end of list is reached, check if we have a playlist to add
    if (i == dir_size):
        if(len(current_files) > 1):
            create_playlist(current_playlist, current_files)
    #Check if file matches any disc file format
    elif(files[i].endswith(FORMATS)):
        file = files[i]
        #First file, nothing to compare it with so it is added to temp playlist
        if(i == 0):
            current_playlist = obtain_pattern(file, symbol)
            current_files.append(file)
        #If name matches, file name added to playlist
        elif(obtain_pattern(file, symbol) == current_playlist):
            current_files.append(file)
        #If no match is found, save the previous playlist and create a new one
        else:
            if(len(current_files) > 1):
                create_playlist(current_playlist, current_files)
            current_playlist = obtain_pattern(file, symbol)
            current_files = [file]
