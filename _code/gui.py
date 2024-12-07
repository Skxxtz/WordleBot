import pygame
from main import prediction
import os
import time


_os = 'Mac' if os.name == 'posix' else 'Windows'
_url = 'C:/Users/sobj2/iCloudDrive/Documents/Programming/Python/wordl/{}' if _os == 'Windows' else '/Users/basti/Desktop/python/wordl/{}'
allowed_words_url = _url.format('_assets/allowed_text.txt')
print(allowed_words_url)





with open(allowed_words_url,'r', encoding='utf-8') as file:
    global allowed_words
    allowed_words =[item.replace('\n','')for item in file.readlines()]
    num_words = len(allowed_words)



pygame.init()
# Set the dimensions of the window
WINDOW_WIDTH, WINDOW_HEIGHT = 640, 480

# Set the font and font size
FONT = pygame.font.SysFont('Arial', 32)
SMALL = pygame.font.SysFont('Arial', 12)
BIG = pygame.font.SysFont('Arial', 52)
# Set the colors
BLACK = (22,22,22)
WHITE = (255, 255, 255)
GRAY = (55, 55, 55)
colors = [[]for _ in range(6)]
color = {
    '0':(165,174,194),
    '1':(236,194,84),
    '2':(135,181,94)
}
d = True
# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


def reset():
    global ROWS,input_list,pos,remaining_words,input_string,pattern,x,d,l,colors
    ROWS = [[pygame.Rect((50+i*55),50+e*55,48,48) for i in range(5)] for e in range(6)]
    colors = [[]for _ in range(6)]
    input_list = ['']
    pos = []
    remaining_words = allowed_words
    input_string = ""
    pattern = ''
    x = 0
    d = True
    l = ''
reset()

while True:
    if x == 12:
        exit()
    # Handle Pygame events
    for event in pygame.event.get():
        # If the user closes the window, exit the program
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # If the user types a key, add it to the input string
        elif event.type == pygame.KEYDOWN and x%2 == 0:
            if event.unicode.isalpha() and len(input_string) < 5:
                input_string += event.unicode.upper()
                if x == 0:
                    input_list[x] = input_string
                else:
                    input_list[int(x/2)] = input_string
            elif event.key == pygame.K_BACKSPACE:
                input_string = input_string[:-1]
                if x == 0:
                    input_list[x] = input_string
                else:
                    input_list[int(x/2)] = input_string
            elif event.key == pygame.K_RETURN and len(input_string) == 5:
                input_list.append('')
                x+=1
        elif event.type == pygame.KEYDOWN and x%2 != 0:
            if event.unicode.isdigit()and event.unicode in ['0','1','2']:
                if x == 0:
                    colors[x].append(color[event.unicode])
                else:
                    colors[int(x/2)].append(color[event.unicode])
                pattern += str(event.unicode)
                
            elif event.key == pygame.K_BACKSPACE and len(pattern)>0:
                pattern = pattern[:-1]
                if x == 0:
                    colors[x].pop(len(colors[x])-1)

                else:
                    colors[int(x/2)].pop(len(colors[int(x/2)])-1)
            elif event.key == pygame.K_RETURN and len(pattern)==5:
                l,pos,words = prediction().predict(sample=input_string.lower(),pattern=pattern,remaining_words=remaining_words)               
                remaining_words = words
                

                x+=1
                if pattern == '22222':
                    d = False
                    reset()
                pattern,input_string = "",""

        
                

            
    # Clear the screen
    def draw():
        window.fill(BLACK)

        # Draw the input box
        for t,row in enumerate(ROWS):
            for i,rec in enumerate(row):
            
                if i<len(colors[t]):
                    pygame.draw.rect(window,colors[t][i],rec) 
                else:
                    pygame.draw.rect(window,(22,22,22),rec)
                pygame.draw.rect(window,GRAY,rec,2)
                
        if l != 0 :
            window.blit(SMALL.render(str(l), True, WHITE),(450,60))

        for t,text in enumerate(input_list):
            for i,letter in enumerate(text):
                window.blit(FONT.render(letter,True,WHITE),(62+i*55,57+t*55))
        for ll,item in enumerate(pos):
                        window.blit(SMALL.render(item[0], True, WHITE),(500,60+30*ll))
                        window.blit(SMALL.render(str(item[1]), True, WHITE),(550,60+30*ll))
        

    # Update the display
    if d == True:
        draw()
    else:
        reset()
        window.fill(BLACK)
        v = BIG.render('WON', True, WHITE)
        window.blit(v,(WINDOW_WIDTH//2-v.get_width()/2,WINDOW_HEIGHT//2-v.get_height()//2))
        pygame.display.update()
        time.sleep(5)
        d = False

    draw()
    pygame.display.update()


    