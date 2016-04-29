#guitar hero!
#you have a box. it has a list of the songs in a directory in your computer
#you chose a song to play
#it will display the words and the chords to the song in a way that allows the user to play along without scrolling

import os, pygame,sys
pygame.init()
def findLocation(bigSpace, font, level =0, directory = "C:\\Users"):
    initalfolders = os.listdir(directory)
    folders = []
    for folder in initalfolders:
        if (folder[len(folder) - 4:-3] != "."):
            folders.append(folder)
            if (folder[len(folder) - 5: -4] == ".") or folder[len(folder)-3:-2] == ".":  #if its actually a file
                folders.remove(folder)
            if folder[:2] == "My":
                folders.remove(folder)

    del initalfolders
    n=0
    littleSpace = pygame.Surface((600,100), 0 ,bigSpace)
    if level ==0:
        header = font.render("which user are you?", True, (0,0,0))
        subheading = font.render("would you like to open a saved directory? press o", True, (0,0,0))
        bigSpace.blit(subheading, (50, bigSpace.get_height() //2))
    else:
        if folders == []:
            header = font.render("please press f", True, (0,0,0))
        else:
            header = font.render("which folder would you like to explore?", True, (0,0,0))
    bigSpace.blit(header, (50,150))
    selecting = True

    while selecting:
        if level == 0:
            Ycoord = 100
        else:
            Ycoord = 200
        addon = 0
        for x in range(len(folders)):
            if x ==n:
                subheading = font.render(folders[x], True, (0,0,255))
            else:
                subheading = font.render(folders[x], True, (0,0,0))
            Xcoord = addon +10 # the x coordinate is the width of the last one plus a little more
            if Xcoord> bigSpace.get_width():
                Ycoord += 50#put it on a new line
                Xcoord = 0
            bigSpace.blit(subheading, (Xcoord, Ycoord))
            addon = subheading.get_width() + Xcoord
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    n +=1
                    if n >=len(folders):
                        n=0
                if event.key == pygame.K_LEFT:
                    n-=1
                    if n <=0:
                        n = len(folders)
                if event.key == pygame.K_RETURN:
                    if level == 0 and folders[n] == "k":
                        directory = directory + "\\" + folders[n] + "\\Documents"
                    elif folders != []:
                        directory = directory + "\\" +folders[n]
                    selecting = False
                    level +=1
                    bigSpace.fill((0,255,0))
                    bigSpace.blit((font.render(directory, True, (0,0,0))), (0,50))
                if event.key == pygame.K_f:
                    dFile = open("savedLocation.txt", "a")
                    dFile.write(directory)
                    dFile.close()
                    firsts(directory)
                if event.key == pygame.K_o:
                    dFile = open("savedLocation.txt", "r")
                    directory = dFile.read()
                    dFile.close()
                    firsts(directory)
                if event.key == pygame.K_UP:
                    level -=1
                    remove = directory.rfind("\\")
                    directory = directory[:remove]
                    bigSpace.fill((0,255,0))
                    bigSpace.blit((font.render(directory, True, (0,0,0))), (0,50))
                    pygame.display.flip()
                    selecting = False
    findLocation(bigSpace, font, level, directory)

def getSongs(directory):
    userFiles  = [] #create a list of possible user files
    listFilter = "txt" #the file extention i need
    for path,d,file in os.walk(directory): #os.walk() returns a tuple hence path, directory,file
        for f in file: # for each file
            if f[-3:] == listFilter: #check the file extention to see if it is txt file
                userFiles.append(f) #if it is, add it into the list!
    return userFiles

def displaySongs(songs, Font, bigSpace,n = 100):
    bigSpace.fill((255,255,255))
    heading = Font.render("use up, down and enter to choose a song", True, (0,0,255))
    songlist = []
    for song in songs:
        if songs.index(song) == n:
            songlist.append(Font.render(song[:-3], True, (0,0,255)))
        else:
            songlist.append(Font.render(song[:-3], True, (0,0,0)))
    bigSpace.blit(heading, (0,0))
    for song in range(len(songs)):
        bigSpace.blit(songlist[song], (0,30*song +50 ))
    pygame.display.flip()


def firsts(directory = None):
    #create a box
    bigSpace = pygame.display.set_mode((750,600),0,32)
    bigSpace.fill((0,255,0))
    #and a font
    font=pygame.font.Font('freesansbold.ttf', 22)
    #get the song titles
    if directory ==None:
        findLocation(bigSpace, font)
    songs = getSongs(directory)
    start( bigSpace, font, songs,directory)


def start(bigSpace, font, songs, directory):
    n = 0
    selected = True
    while selected:
        #for all events
        for event in pygame.event.get():
                #if the event is to quit
                if event.type == pygame.QUIT:
                    #then QUIT
                    pygame.display.quit()
                    sys.exit()
                #if the event is the down key
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                    #highlight the one below
                        n +=1
                        if n>len(songs):
                            n = 0
                #if the event is the up key
                    if event.key== pygame.K_UP:
                    #highlight the one above
                        n -=1
                        if n < 0:
                            n= len(songs)
                #if the event is ENTER then
                    if event.key == pygame.K_RETURN:
                    # song selected = this song!!
                        selectedSong = songs[n]
                        selected = False
        #refresh the box.
        displaySongs(songs, font,bigSpace, n )
    running(songs,bigSpace,n, font, directory)
def displaylyrics( lyrics,bigSpace):
    for lyric in lyrics:
        bigSpace.blit(lyric[0], lyric[1])
        x,y = lyric[1]
        lyric[1] = (x, y-25 )
    pygame.display.flip()
    bigSpace.fill((255,255,255))

def running(songs,bigSpace,n, font, directory):
    playing = open(directory + "\\"+ songs[n], 'r')
    chords = playing.readlines()
    lyrics = []
    a = 0
    for x in chords:
        if x != "":
            lyrics.append([font.render(x[:-1], True, (0,0,0)), (0,50*a+bigSpace.get_height())])
        a +=1
    x =0    #top line being shown
    display = bigSpace.get_height() //4
    waitTime = 700
    while lyrics[len(lyrics)-1][1] != (0,0):
            displaylyrics(lyrics, bigSpace, )
            for event in pygame.event.get():
                    #if the event is to quit
                    if event.type == pygame.QUIT:
                    #then QUIT
                        pygame.display.quit()
                        sys.exit()
                        playing.close()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            waitTime -=10
                        if event.key == pygame.K_DOWN:
                            waitTime +=10
            pygame.time.wait(waitTime)
            x +=1
    start(bigSpace, font, songs, directory)
bigSpace, font,songs, directory = firsts()
start(bigSpace, font, songs, directory)
