"""
    In Alien Invasion, the player controls a rocket ship, which is displayed in the lower center of the screen. 
    The player can move the ship right and left using the arrow keys and fire bullets using the space bar. 
    When the game starts, a fleet of aliens fills the sky and moves down the screen. 
    The player shoots and destroys the aliens. If the player destroys all the aliens, a new fleet appears, which moves faster than the previous fleet. 
    If any alien hits the player's ship or reaches the bottom of the screen, the player loses the ship. 
    If a player loses three ships, it's game over.
"""

import sys
from time import sleep
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion: 
    
    def __init__(self):
        #initialize the game, and create game resources
        pygame.init()
        
        self.clock = pygame.time.Clock() # frame rate -> da sat otkucava jednako kroz svaku petlju da bi igra radila konstantom brzinom
        self.settings = Settings()
        
        #self.screen = pygame.display.set_mode((1200, 800))
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        #self.bg_color = (230, 230, 230) # RGB, crvena, plava i zelena
        self.game_active = True
        
    def run_game(self):
        #Start the main loop for the game
        while True:
            if self.game_active : 
                self._check_events()
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()                    
            self.clock.tick(60) # brzina smenjivanja kadrova za igru, petlja pokrenuta tacno 50 puta u petlji
            
    def _check_events(self):
        # Respond to keypresses and mouse events.
        for event in pygame.event.get(): # pygame.event.get() kupi unos sa tastature
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
                    
    def _check_keydown_events(self, event):
        # Respond to keypresses
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True   
        elif event.key == pygame.K_q:
            sys.exit() 
        elif event.key == pygame.K_SPACE:
            self._fire_bulet()
    
    def _check_keyup_events(self, event):
        # Respont to key releases.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    def _fire_bulet(self):
        # Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
                
    def _update_screen(self):
        # Update images on the screen, and flip to the new screen.
        self.screen.fill(self.settings.bg_color) # .fill popunjavamo boju pozadine
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip() # flip() prikazu poslednji ekran koji vidi
        
    def _update_bullets(self):
        self.bullets.update()
            
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
            
        self._check_bullet_alien_collision()
        
    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            
            current_x = alien_width
            current_y += 2 * alien_height
            
    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
            
        self._check_aliens_bottom()
        
    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1
        
    def _check_bullet_alien_collision(self):
        # Check for any bullets that have hit aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
        
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            
            self.bullets.empty()
            self.aliens.empty()
            
            self._create_fleet()
            self.ship.center_ship()
            
            sleep(0.5)
        else:
            self.game_active = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        
    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
                
if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()