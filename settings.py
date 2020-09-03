import pygame

vec = pygame.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (104, 243, 243)

# game settings
WIDTH = 1024  # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 120
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen.png'

PLAYER_HEALTH = 100
PLAYER_ARMOUR = 100
PLAYER_SPEED = 300
PLAYER_ROT_SPEED = 250  # Deg per sec
PLAYER_IMGS = {'ak47': 'player_ak47.png',
               'saved_off': 'player_soff.png',
               'p2k': 'player_p2k.png'}
PLAYER_IMGS_KEVLAR = {'p2k': 'player_kevlar_p2k.png',
                      'ak47': 'player_kevlar_ak47.png',
                      'saved_off': 'player_kevlar_soff.png'}

PLAYER_HIT_RECT = pygame.Rect(0, 0, 37, 37)
BARREL_OFFSET = vec(23, 11)
KICKBACK = 200
GUN_SPREAD = 7

# Gun settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['p2k'] = {'bullet_speed': 550,
                  'bullet_lifetime': 1000,
                  'rate': 250,
                  'bullet_damage': 10,
                  'kickback': 200,
                  'spread': 7,
                  'bullet_size': 'lg',
                  'bullet_count': 1,
                  'player_speed': 300,
                  'ammo': 60,
                  'max_ammo': 180,
                  'player_img': 'player_kevlar_rifle.png'}
WEAPONS['saved_off'] = {'bullet_speed': 400,
                        'bullet_lifetime': 500,
                        'rate': 900,
                        'bullet_damage': 5,
                        'kickback': 1000,
                        'spread': 20,
                        'bullet_size': 'sm',
                        'bullet_count': 12,
                        'player_speed': 200,
                        'ammo': 20,
                        'max_ammo': 60,
                        'player_img': 'player_shotgun.png'}
WEAPONS['ak47'] = {'bullet_speed': 650,
                   'bullet_lifetime': 1200,
                   'rate': 100,
                   'bullet_damage': 8,
                   'kickback': 150,
                   'spread': 2,
                   'bullet_size': 'sm',
                   'bullet_count': 1,
                   'player_speed': 250,
                   'ammo': 90,
                   'max_ammo': 300,
                   'player_img': 'player_rifle.png'}

# Mob settings
ZOMBIE_IMG = 'zoimbie1_hold.png'
ZOMBIE_HIT_RECT = pygame.Rect(0, 0, 35, 35)
ZOMBIE_HEALTH = 70
ZOMBIE_DAMAGE = 10
ZOMBIE_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400
MOB_SPEED = [125, 150, 175, 200]

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 40
SPLAT_IMG = 'splat green.png'
BROKEN_GLASS = 'broken_glass.png'
BROKEN_DOOR = 'broken_door.png'
DMG_APLHA = [i for i in range(0, 255, 25)]  # We get a list of i's
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = 'light_350_hard.png'

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'p2k': 'p2k.png',
               'saved_off': 'saved_off.png',
               'ak47': 'ak47.png',
               'kevlar': 'vest.png',
               'ammo_box': 'ammo_box.png',
               'bullets': 'bullets.png'}
HEALTH_REFILL = 30
BOB_RANGE = 15
BOB_SPEED = 0.25

# destructible obstacles

DEST_OBS_IMAGES = {'window_h': 'window_h.png',
                   'window_v': 'window_v.png',
                   'door_h': 'door_h.png',
                   'door_v': 'door_v.png'}

# HUD settings
GUN_CIRCLE_FILL = (184, 14, 15)
GUN_CIRCLE_CENTER = (260, 40)
BG_RECT_FILL = (128, 115, 122)
KEVLAR_COLOR = (27, 99, 213)

# Sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'p2k': ['pistol.wav'],
                 'saved_off': ['shotgun.wav'],
                 'ak47': ['pistol.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'broken_glass': 'glass_break.wav',
                  'broken_door': 'wood_break.wav',
                  'hit_door': 'door_hit.wav'}
