#guitar hero!
#you have a box. it has a list of the songs in a directory in your computer
#you chose a song to play
#it will display the words and the chords to the song in a way that allows the user to play along without scrolling

import os, pygame,sys
pygame.init()
def getSongs():
    userFiles  = [] #create a list of possible user files
    listFilter = "txt" #the file extention i need
    for path,directory,file in os.walk('C:\\Users\\k\\Documents\\music'): #os.walk() returns a tuple hence path, directory,file
        for f in file: # for each file
            if f[-3:] == listFilter: #check the file extention to see if it is txt file
                userFiles.append(f) #if it is, add it into the list!
    print(userFiles)
    return userFiles

def displaySongs(songs, Font, n = 100):
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
def displaylyrics(bigSpace, lyrics, x, w ):
    for y in range(7):
        if y +x <len(lyrics):
            bigSpace.blit(lyrics[x+y], (50, 50*y +50 - 10*w))
            #flip the screen
    pygame.display.flip()
    #wait a few seconds
    pygame.time.wait(375)
    # clear the box
    bigSpace.fill((255,255,255))

def firsts():
    #create a box
    bigSpace = pygame.display.set_mode((600,400),0,32)
    bigSpace.fill((0,255,0))
    #and a font
    font=pygame.font.Font('freesansbold.ttf', 22)
    #get the song titles
    songs = getSongs()
    return bigSpace, font, songs


def start(bigSpace, font, songs):
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
        displaySongs(songs, font, n)
    running(songs,bigSpace,n)

def running(songs,bigSpace,n):
    playing = open('C:\\Users\\k\\Documents\\music\\'+ songs[n], 'r')
    chords = playing.readlines()
    lyrics = [font.render((""), True, (0,0,0)) for s in range(4) ]
    for x in chords:
        if x != "":
            lyrics.append(font.render(x[:-1], True, (0,0,0)))
    x =0
    while x<len(lyrics):
        #blit the text (chords/ lyrics) 5 lines
            displaylyrics(bigSpace, lyrics,x, 0 )   #5 lyrics in first location
            displaylyrics(bigSpace, lyrics, x, 1 )
            displaylyrics(bigSpace, lyrics, x, 2 )
            displaylyrics(bigSpace, lyrics, x, 3 )
            for event in pygame.event.get():
                    #if the event is to quit
                    if event.type == pygame.QUIT:
                    #then QUIT
                        pygame.display.quit()
                        sys.exit()
                        playing.close()
            x +=1
bigSpace, font,songs = firsts()
start(bigSpace, font, songs)
