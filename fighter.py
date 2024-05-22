import pygame

class Fighter():
    def __init__(self, player, x, y, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = self.load_img(sprite_sheet, animation_steps)
        self.action = 0 # 0 = idle; 1 run; 2 jump ; 3 attack1; 4 atk2 ; 5 hit; 6 death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_vert = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.atk_type = 0
        self.atk_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_img(self, sprite_sheet, animation_steps):
        #extract from sprite sheet
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)

                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.atk_type = 0

        #keys
        key = pygame.key.get_pressed()

        #actions only if you are not attacking
        if self.attacking == False and self.alive == True and round_over == False:
            #check player1 controls
            if self.player == 1:
                #movement
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_d]:
                    dx = SPEED
                    self.running = True
                #jump
                if key[pygame.K_w] and self.jump == False:
                    self.vel_vert = -30
                    self.jump = True
                #attack
                if key[pygame.K_q] or key[pygame.K_e]:
                    self.attack(target)
                    if key[pygame.K_q]:
                        self.atk_type = 1
                    if key[pygame.K_e]:
                        self.atk_type = 2

            # check player2 controls
            if self.player == 2:
                # movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                # jump
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_vert = -30
                    self.jump = True
                # attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    if key[pygame.K_KP1]:
                        self.atk_type = 1
                    if key[pygame.K_KP2]:
                        self.atk_type = 2

        #gravity
        self.vel_vert += GRAVITY
        dy += self.vel_vert

        #player on screen limits
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right

        if self.rect.bottom + dy > screen_height -110:
            self.vel_vert = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        #players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        #cooldown
        if self.atk_cooldown > 0:
            self.atk_cooldown -= 1

        #update position
        self.rect.x += dx
        self.rect.y += dy

    #animation updates
    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        elif self.hit == 1:
            self.update_action(5)
        elif self.attacking == True:
            if self.atk_type == 1:
                self.update_action(3)
            elif self.atk_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)


        cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            # dead?
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                if self.action == 3 or self.action ==4:
                    self.attacking = False
                    self.atk_cooldown = 20
                #was dmg taken?
                if self.action == 5:
                    self.hit = False
                    #contra?
                    self.attacking = False
                    self.atk_cooldown = 20


    def attack(self, target):
        if self.atk_cooldown == 0:
            self.attacking = True
            atk_area = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if atk_area.colliderect(target.rect):
                target.health -= 10
                target.hit = True


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        im = pygame.transform.flip(self.image, self.flip,False)
        surface.blit(im, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
