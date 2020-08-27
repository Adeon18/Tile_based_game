# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 7
# Mobs
# Video link: https://youtu.be/gbRAqFl21SA
import pygame
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.scr_width, self.scr_height = pygame.display.get_surface().get_size()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        effects_folder = path.join(img_folder, 'effects')
        item_folder = path.join(img_folder, 'items')
        player_folder = path.join(img_folder, 'player')
        zombie_folder = path.join(img_folder, 'zombie')
        self.map_folder = path.join(game_folder, 'maps')
        self.dim_screen = pygame.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.player_imgs = {}
        for item in PLAYER_IMGS:
            self.player_imgs[item] = pygame.image.load(path.join(player_folder, 
                                                                 PLAYER_IMGS[item])).convert_alpha()
        self.player_imgs_kevlar = {}
        for item in PLAYER_IMGS_KEVLAR:
            self.player_imgs_kevlar[item] = pygame.image.load(path.join(player_folder, 
                                                                        PLAYER_IMGS_KEVLAR[item])).convert_alpha()

        self.zombie_img = pygame.image.load(path.join(zombie_folder, ZOMBIE_IMG)).convert_alpha()
        self.bullet_imgs = {}
        self.bullet_imgs['lg'] = pygame.image.load(path.join(item_folder, BULLET_IMG)).convert_alpha()
        self.bullet_imgs['sm'] = pygame.transform.scale(self.bullet_imgs['lg'], (10, 10))
        self.splat = pygame.image.load(path.join(effects_folder, SPLAT_IMG)).convert_alpha()
        self.splat = pygame.transform.scale(self.splat, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pygame.image.load(path.join(effects_folder, img)).convert_alpha())
        self.item_imgs = {}
        for item in ITEM_IMAGES:
            self.item_imgs[item] = pygame.image.load(path.join(item_folder, ITEM_IMAGES[item])).convert_alpha()
        # Lighting effect
        self.fog = pygame.Surface((self.scr_width, self.scr_height))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pygame.image.load(path.join(effects_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pygame.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        pygame.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pygame.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.effects_sounds['level_start'].set_volume(0.05)
        self.effects_sounds['gun_pickup'].set_volume(0.05)

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pygame.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.05)
                self.weapon_sounds[weapon].append(s)

        self.zombie_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.1)
            self.zombie_sounds.append(s)

        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.4)
            self.player_hit_sounds.append(s)

        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pygame.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_hit_sounds.append(s)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        '''for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)'''
        self.map = TiledMap(path.join(self.map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name in ['health', 'saved_off', 'ak47', 'kevlar']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self, self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False

        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pygame.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pygame.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # Game over
        if len(self.mobs) == 0:
            self.playing = False
        # Player hits items
        hits = pygame.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_REFILL)
                self.effects_sounds['health_up'].play()
            if hit.type == 'saved_off':
                try:
                    if 'saved off' not in self.player.weapons['shotgun']:
                        pass
                except KeyError:
                    hit.kill()
                    self.player.weapon = 'saved_off'
                    self.player.weapons.update(shotgun='saved_off')
                    self.effects_sounds['gun_pickup'].play()
            if hit.type == 'ak47':
                try:
                    if 'ak47' not in self.player.weapons['rifle']:
                        pass
                except KeyError:
                    hit.kill()
                    self.player.weapon = 'ak47'
                    self.player.weapons.update(rifle='ak47')
                    self.effects_sounds['gun_pickup'].play()
            if hit.type == 'kevlar' and self.player.armour < PLAYER_ARMOUR:
                hit.kill()
                self.player.armour = PLAYER_ARMOUR
                self.effects_sounds['gun_pickup'].play()

        # Mobs hit player
        hits = pygame.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if self.player.armour > 0:
                self.player.armour -= ZOMBIE_DAMAGE
            else:
                self.player.health -= ZOMBIE_DAMAGE
            hit.vel = (0, 0)
            if self.player.health <= 0:
                self.playing = False
            # Sound
            if random.random() < 0.7:
                random.choice(self.player_hit_sounds).play()
        if hits:
            self.player.hit()
            self.player.pos += vec(ZOMBIE_KNOCKBACK, 0).rotate(-hits[0].rot)

        # Bullets hit mobs
        hits = pygame.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for mob in hits:
            #hit.health -= WEAPONS[self.player.weapon]['bullet_damage'] * len(hits[hit])
            for bullet in hits[mob]:
                mob.health -= bullet.damage
            mob.vel = (0, 0)
            mob.hit()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pygame.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pygame.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
            self.draw_text("{:.2f}".format(self.clock.get_fps()), 25, CYAN, self.scr_width / 2, 30)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()
        # HUD funcs
        self.draw_hud()
        # What to draw if paused
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text('Paused', 105, RED, self.scr_width / 2, self.scr_height / 2)
        pygame.display.flip()

    def events(self):
        # catch all events here
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F4:
                    self.quit()
                if event.key == pygame.K_F3:
                    self.draw_debug = not self.draw_debug
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_F2:
                    self.night = not self.night

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text('GAME OVER', 100, RED, self.scr_width / 2, self.scr_height / 2)
        self.draw_text('Press a key to start', 75, WHITE,
                       self.scr_width / 2, 3 * self.scr_height / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pygame.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y, align='center'):
        font = pygame.font.Font('fonts/ZOMBIE.ttf', size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def render_fog(self):
        # Draw light mask (gradient) onto fog img
        self.fog.fill(NIGHT_COLOR)
        #self.light_rect.center = self.player.pos
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw_hud(self):
        self.draw_hud_bg()
        self.draw_player_health(0, 0, self.player.health / PLAYER_HEALTH)
        self.draw_armour_health(0, 25, self.player.armour / PLAYER_ARMOUR)
        self.draw_current_gun()
        self.draw_text('Zombies-{}'.format(len(self.mobs)), 30, BLACK, self.scr_width - 50, 50, align='ne')

    def draw_player_health(self, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 110
        BAR_HEIGHT = 25
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = (x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            col = GREEN
        elif pct > 0.3:
            col = YELLOW
        else:
            col = RED
        pygame.draw.rect(self.screen, col, fill_rect)
        pygame.draw.rect(self.screen, BLACK, outline_rect, 3)
        self.draw_text('health', 20, BLACK, outline_rect.centerx, outline_rect.centery + 3)

    def draw_current_gun(self):
        # Get the current weapon and resize it for the icon
        weapon_icon = pygame.transform.scale(self.item_imgs[self.player.weapon], (48, 48))
        weapon_rect = weapon_icon.get_rect()
        weapon_rect.center = GUN_CIRCLE_CENTER
        self.draw_text('{}'.format(self.player.weapon), 24, BLACK, 115, 1, 'nw')
        self.screen.blit(weapon_icon, weapon_rect)

    def draw_hud_bg(self):
        # Bg rect and outline
        bg_rect = pygame.Rect(0, 0, 300, 80)
        bg_rect_outline = pygame.Rect(0, 0, 300, 80)
        pygame.draw.rect(self.screen, BG_RECT_FILL, bg_rect)
        pygame.draw.rect(self.screen, BLACK, bg_rect_outline, 3)
        # Circle and outline
        pygame.draw.circle(self.screen, GUN_CIRCLE_FILL, GUN_CIRCLE_CENTER, 35)
        pygame.draw.circle(self.screen, BLACK, GUN_CIRCLE_CENTER, 36, 3)

    def draw_armour_health(self, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 110
        BAR_HEIGHT = 25
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = (x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, KEVLAR_COLOR, fill_rect)
        pygame.draw.rect(self.screen, BLACK, outline_rect, 3)
        self.draw_text('armour', 20, BLACK, outline_rect.centerx, outline_rect.centery + 3)



# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
