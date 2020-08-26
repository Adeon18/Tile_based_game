import pygame
import random
import pytweening
import itertools
from settings import *
from tilemap import collide_hit_rect
vec = pygame.math.Vector2


def collide_with_walls(sprite, group, direction):
    if direction == 'x':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if direction == 'y':
        hits = pygame.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_pistol
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH
        self.weapons = ['pistol']
        self.weapon = 'pistol'
        self.c = itertools.cycle(self.weapons)
        self.damaged = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rot_speed = PLAYER_ROT_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rot_speed = -PLAYER_ROT_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel = vec(WEAPONS[self.weapon]['player_speed'], 0).rotate(-self.rot)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel = vec(-WEAPONS[self.weapon]['player_speed'] / 2, 0).rotate(-self.rot)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_1]:
            self.weapon = self.weapons[0]
        if keys[pygame.K_2]:
            try:
                self.weapon = self.weapons[1]
            except IndexError:
                pass
        if keys[pygame.K_3]:
            try:
                self.weapon = self.weapons[2]
            except IndexError:
                pass


    def update(self):
        self.get_keys()
        self.image = self.game.player_imgs[self.weapon]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pygame.transform.rotate(self.image, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pygame.BLEND_RGBA_MULT)
            except StopIteration:
                self.damaged = False

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            direction = vec(1, 0).rotate(-self.rot)
            # KIck the player back when shooting
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)

            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = random.uniform(-WEAPONS[self.weapon]['spread'],
                                         WEAPONS[self.weapon]['spread'])  # Spread in degrees
                Bullet(self.game, pos, direction.rotate(spread), WEAPONS[self.weapon]['bullet_damage'])
                snd = random.choice(self.game.weapon_sounds[self.weapon])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            MuzzleFlash(self.game, pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = itertools.chain(DMG_APLHA * 3)


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.zombie_img.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = ZOMBIE_HIT_RECT.copy()
        self.rect.center = (x, y)
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.speed = random.choice(MOB_SPEED)
        self.health = ZOMBIE_HEALTH
        self.target = self.game.player
        self.damaged = False

    def update(self):
        target_dist = self.game.player.pos - self.pos
        # Calculating sqrt is slow
        if target_dist.length_squared() < DETECT_RADIUS ** 2 or self.health < ZOMBIE_HEALTH:
            if random.random() < 0.002:
                random.choice(self.game.zombie_sounds).play()
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pygame.transform.rotate(self.game.zombie_img, self.rot)
            if self.damaged:
                try:
                    self.image.fill((0, 255, 0, next(self.damage_alpha)), special_flags=pygame.BLEND_RGB_MULT)
                except StopIteration:
                    self.damaged = False
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += (-self.vel[0], -self.vel[1])
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')

        if self.health <= 0:
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
            random.choice(self.game.zombie_hit_sounds).play()

    def draw_health(self):
        if self.health > ZOMBIE_HEALTH // 1.5:
            col = GREEN
        elif self.health > ZOMBIE_HEALTH // 3:
            col = YELLOW
        else:
            col = RED

        width = int(self.rect.width * self.health / ZOMBIE_HEALTH)
        self.health_bar = pygame.Rect(0, 0, width, 7)
        if self.health < ZOMBIE_HEALTH:
            pygame.draw.rect(self.image, col, self.health_bar)

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                distance = self.pos - mob.pos
                if 0 < distance.length() < AVOID_RADIUS:
                    self.acc += distance.normalize()  # Make the dist the len of 1

    def hit(self):
        self.damaged = True
        self.damage_alpha = itertools.chain(DMG_APLHA * 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, pos, direction, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.bullet_imgs[WEAPONS[self.game.player.weapon]['bullet_size']]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)  # Pos copy
        self.rect.center = pos
        self.damage = damage
        self.vel = direction * WEAPONS[self.game.player.weapon]['bullet_speed'] * random.uniform(0.9, 1.1)
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos

        hits = pygame.sprite.spritecollideany(self, self.game.walls, False)
        if pygame.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime'] or hits:
            self.kill()


class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width, height):
        self._layer = WALL_LAYER
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y


class MuzzleFlash(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.size = random.randint(20, 30)
        self.image = pygame.transform.scale(random.choice(game.gun_flashes), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pygame.time.get_ticks()

    def update(self):
        if pygame.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()


class Item(pygame.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = type
        self.pos = pos
        self.image = self.game.item_imgs[self.type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.rect.center = pos
        self.tween = pytweening.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # Bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1
