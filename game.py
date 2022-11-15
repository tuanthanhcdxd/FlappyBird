import pygame, sys, random

# tao ham cho tro choi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650)) # set goc toa do cua floor image trong man hinh game
    screen.blit(floor, (floor_x_pos+432, 650)) # set goc toa do cua san thu 2 floor image trong man hinh game

def create_pipe(): # ham tao ong
    random_pipe_pos = random.choice(pipe_height) # chon random chieu cao cho ong
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos)) # tao ong moi se xuat hien o vi tri 500 va 1 vi tri random
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos-700)) # tao ong moi se xuat hien o vi tri 500 va 1 vi tri random
    return bottom_pipe, top_pipe

def move_pipe(pipes): # tao ham khi ong di chuyen
    for pipe in pipes: # cho pipe trong mot danh sach ong
        pipe.centerx -= 4 # ong se di chuyen lui ve 4 don vi
    return pipes  # sau do ong lai di chuyen ve vi tri 500

def draw_pipe(pipes): # tao ham hien thi ong
    for pipe in pipes: # cho pipe trong danh sach ong
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe) # pipe hien thi ong tren man hinh game
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes): # tao ham xu ly va cham
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1) # tao hieu ung xoay cho chim
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216, 630))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432, 768)) # set man hinh game
clock = pygame.time.Clock() # set fps cho man hinh
game_font = pygame.font.Font('04B_19.ttf', 40)

# tao bien cho tro choi
gravity = 0.25 # set trong luc cho bird
bird_movement = 0 # set di chuyen cua bird
game_active = True
score = 0
high_score = 0

bg = pygame.image.load('assests/background-night.png').convert() # set background game, chen them convert cho anh duoc load nhanh hon
bg = pygame.transform.scale2x(bg) # scale background len 2 lan

floor = pygame.image.load('assests/floor.png').convert() # set floor image
floor = pygame.transform.scale2x(floor) # scale floor image len 2 lan
floor_x_pos = 0 # set toa do cua floor theo vi tri nhan vat theo truc x

bird_down = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-downflap.png')).convert_alpha()
bird_mid = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-midflap.png')).convert_alpha()
bird_up = pygame.transform.scale2x(pygame.image.load('assests/yellowbird-upflap.png')).convert_alpha()
bird_list = [bird_down, bird_mid, bird_up]
bird_index = 0
bird = bird_list[bird_index]
# bird = pygame.image.load('assests/yellowbird-midflap.png').convert_alpha() # set bird image
# bird = pygame.transform.scale2x(bird) # scale bird image len 2 lan
bird_rect = bird.get_rect(center=(100, 300)) # set hinh chu nhat de dat bird vao

# tao timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)

pipe_surface = pygame.image.load('assests/pipe-green.png').convert() # set duong ong
pipe_surface = pygame.transform.scale2x(pipe_surface) # scale pipe image len 2 lan
pipe_list = []

spawnpipe = pygame.USEREVENT # tao timer xuat hien pipe
pygame.time.set_timer(spawnpipe, 1200) # set sau 1,2 s se tao ra ong moi
pipe_height = [300,350,400] # set chieu dai ong mac dinh trong khoang nay
# tao man hinh ket thuc
game_over_surface = pygame.transform.scale2x(pygame.image.load('assests/message.png')).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(216, 384))

# chen am thanh
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100



while True: # tao vong lap lien tuc de hien thi game

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # set lenh khi quit game
            pygame.quit()
            sys.exit() # set lenh nay neu khong muon hien thong bao loi
        if event.type == pygame.KEYDOWN: # set lenh khi phim bat ky duoc an
            if event.key == pygame.K_SPACE and game_active: # set lenh khi phim duoc an la SPACE
                bird_movement = 0 # set gia tri bang 0
                bird_movement = -8 # set gia tri bang 8 khi an space
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe: # set lenh ong se xuat hien sau 1 khoang thoi gian
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        
            bird, bird_rect = bird_animation()

            

    screen.blit(bg, (0, 0)) # set goc toa do cua back ground trong man hinh game
    if game_active:
        #chim
        bird_movement += gravity # set khi bird di chuyen thi trong luc tang theo
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement # set khi chim di chuyen xuong duoi thi rec cung di chuyen xuong theo
        screen.blit(rotated_bird, bird_rect) # set goc toa do cua bird trong man hinh game
        game_active = check_collision(pipe_list)
        #ong
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display('main game')
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100

    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')
    #san
    floor_x_pos -= 1 # gia tri x giam dan theo moi vong lap
    draw_floor()

    if floor_x_pos <= -432: # new toa do cua x chay het chieu rong man hinh
        floor_x_pos = 0 # ta set lai toa do cua no bang 0

    pygame.display.update() # hien thi thao tac hoan tat
    clock.tick(120) # set fps 120
