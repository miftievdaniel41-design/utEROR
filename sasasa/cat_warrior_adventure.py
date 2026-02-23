import pygame
import sys
import random
import os
import json
import traceback
from datetime import datetime

# ... (код создания папок и обработки исключений остается таким же) ...

# Улучшенная система модов с проверкой ошибок
class ModSystem:
    def __init__(self):
        self.weapons = {}
        self.active_weapon = "pistol"
        self.load_weapons()
    
    def load_weapons(self):
        """Загрузка оружия с улучшенной обработкой ошибок"""
        try:
            # Базовое оружие
            self.weapons = {
                "pistol": {
                    "name": "🔫 Пистолет",
                    "damage": 10,
                    "speed": 10,
                    "color": (255, 255, 0),  # YELLOW как tuple
                    "cooldown": 15,
                    "bullet_size": [8, 16]
                }
            }
            
            # Загрузка модов оружия
            weapons_dir = FOLDERS.get("mods_weapons", "")
            if os.path.exists(weapons_dir):
                for file in os.listdir(weapons_dir):
                    if file.endswith(".json"):
                        try:
                            filepath = os.path.join(weapons_dir, file)
                            with open(filepath, "r", encoding="utf-8") as f:
                                weapon_data = json.load(f)
                            
                            weapon_name = file.replace(".json", "")
                            
                            # Корректная обработка цвета
                            if "color" in weapon_data:
                                if isinstance(weapon_data["color"], list):
                                    weapon_data["color"] = tuple(weapon_data["color"])
                                else:
                                    # Если цвет некорректный, используем желтый
                                    weapon_data["color"] = (255, 255, 0)
                            else:
                                weapon_data["color"] = (255, 255, 0)
                            
                            # Устанавливаем значения по умолчанию
                            weapon_data.setdefault("damage", 10)
                            weapon_data.setdefault("speed", 10)
                            weapon_data.setdefault("cooldown", 15)
                            weapon_data.setdefault("bullet_size", [8, 16])
                            
                            self.weapons[weapon_name] = weapon_data
                            print(f"✅ Загружено оружие: {weapon_data['name']}")
                            
                        except Exception as e:
                            print(f"❌ Ошибка загрузки оружия {file}: {e}")
                            # Создаем базовое оружие как запасной вариант
                            self.weapons[file.replace(".json", "")] = {
                                "name": f"Оружие {file}",
                                "damage": 10,
                                "speed": 10,
                                "color": (255, 255, 0),
                                "cooldown": 15,
                                "bullet_size": [8, 16]
                            }
            
            print(f"🎯 Всего оружия: {len(self.weapons)}")
            
        except Exception as e:
            print(f"💥 Критическая ошибка загрузки оружия: {e}")
            # Создаем хотя бы базовое оружие
            self.weapons = {
                "pistol": {
                    "name": "🔫 Пистолет",
                    "damage": 10,
                    "speed": 10,
                    "color": (255, 255, 0),
                    "cooldown": 15,
                    "bullet_size": [8, 16]
                }
            }
    
    def get_current_weapon(self):
        """Получение текущего оружия с защитой от ошибок"""
        try:
            return self.weapons.get(self.active_weapon, self.weapons["pistol"])
        except:
            return {
                "name": "🔫 Пистолет",
                "damage": 10,
                "speed": 10,
                "color": (255, 255, 0),
                "cooldown": 15,
                "bullet_size": [8, 16]
            }
    
    def switch_weapon(self, weapon_name):
        """Переключение оружия с улучшенной обработкой ошибок"""
        try:
            if weapon_name in self.weapons:
                self.active_weapon = weapon_name
                weapon_data = self.weapons[weapon_name]
                print(f"🎯 Оружие изменено на: {weapon_data['name']}")
                return True
            else:
                print(f"⚠️ Оружие '{weapon_name}' не найдено")
                return False
        except Exception as e:
            print(f"💥 Ошибка переключения оружия: {e}")
            return False

# ... (остальные классы Bullet, Player, Enemy, Boss остаются в основном те же) ...

# Улучшенный класс Game с исправленной обработкой событий
class Game:
    def __init__(self):
        # ... (инициализация как раньше) ...
        self.weapon_change_cooldown = 0  # Задержка между сменой оружия
        
    def handle_event(self, event):
        """Улучшенный обработчик событий с защитой от ошибок"""
        try:
            if event.type == pygame.KEYDOWN:
                print(f"🔑 Нажата клавиша: {event.key}")  # Отладочная информация
                
                # Обработка выхода
                if event.key == pygame.K_ESCAPE:
                    if self.game_state in ["weapons_menu", "game_over"]:
                        self.game_state = "menu"
                    elif self.game_state == "playing":
                        self.game_state = "menu"
                    return
                
                # Обработка паузы/меню
                if event.key == pygame.K_p:
                    if self.game_state == "playing":
                        self.game_state = "paused"
                    elif self.game_state == "paused":
                        self.game_state = "playing"
                    return
                
                # Проверяем задержку смены оружия
                if self.weapon_change_cooldown > 0:
                    return
                
                # Основные действия по состояниям игры
                if self.game_state == "menu":
                    self.handle_menu_events(event)
                elif self.game_state == "playing":
                    self.handle_playing_events(event)
                elif self.game_state == "weapons_menu":
                    self.handle_weapons_menu_events(event)
                elif self.game_state == "game_over":
                    self.handle_game_over_events(event)
                elif self.game_state == "paused":
                    self.handle_paused_events(event)
                    
        except Exception as e:
            print(f"💥 Ошибка в обработчике событий: {e}")
            traceback.print_exc()
    
    def handle_menu_events(self, event):
        """Обработка событий в главном меню"""
        if event.key == pygame.K_SPACE:
            self.reset_game()
            self.game_state = "playing"
            print("🚀 Игра началась!")
        elif event.key == pygame.K_w:
            self.game_state = "weapons_menu"
            print("🎯 Открыто меню оружия")
        elif event.key == pygame.K_i:
            self.show_game_info()
    
    def handle_playing_events(self, event):
        """Обработка событий во время игры"""
        if event.key == pygame.K_SPACE:
            self.player.shoot()
            print("💥 Выстрел!")
        
        # Смена оружия цифрами (1-9)
        elif pygame.K_1 <= event.key <= pygame.K_9:
            weapon_index = event.key - pygame.K_1
            weapons_list = list(mod_system.weapons.keys())
            
            if weapon_index < len(weapons_list):
                weapon_name = weapons_list[weapon_index]
                if mod_system.switch_weapon(weapon_name):
                    self.weapon_change_cooldown = 10  # Задержка 10 кадров
                    print(f"🔧 Оружие изменено на индекс {weapon_index}: {weapon_name}")
            else:
                print(f"⚠️ Оружие с индексом {weapon_index} не существует")
        
        # Циклическая смена оружия (Q)
        elif event.key == pygame.K_q:
            weapons_list = list(mod_system.weapons.keys())
            if weapons_list:
                current_index = weapons_list.index(mod_system.active_weapon)
                next_index = (current_index + 1) % len(weapons_list)
                weapon_name = weapons_list[next_index]
                if mod_system.switch_weapon(weapon_name):
                    self.weapon_change_cooldown = 10
                    print(f"🔄 Циклическое переключение на: {weapon_name}")
        
        # Пауза
        elif event.key == pygame.K_p:
            self.game_state = "paused"
            print("⏸️ Игра на паузе")
    
    def handle_weapons_menu_events(self, event):
        """Обработка событий в меню оружия"""
        if event.key == pygame.K_w or event.key == pygame.K_ESCAPE:
            self.game_state = "menu"
            print("📋 Возврат в главное меню")
        
        # Выбор оружия цифрами
        elif pygame.K_1 <= event.key <= pygame.K_9:
            weapon_index = event.key - pygame.K_1
            weapons_list = list(mod_system.weapons.keys())
            
            if weapon_index < len(weapons_list):
                weapon_name = weapons_list[weapon_index]
                if mod_system.switch_weapon(weapon_name):
                    print(f"✅ В меню оружия выбран: {weapon_name}")
            else:
                print(f"⚠️ В меню оружия: индекс {weapon_index} вне диапазона")
    
    def handle_game_over_events(self, event):
        """Обработка событий при game over"""
        if event.key == pygame.K_r:
            self.reset_game()
            self.game_state = "playing"
            print("🔄 Игра перезапущена")
        elif event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
            self.game_state = "menu"
            print("📋 Возврат в меню после проигрыша")
    
    def handle_paused_events(self, event):
        """Обработка событий в режиме паузы"""
        if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
            self.game_state = "playing"
            print("▶️ Продолжение игры")
        elif event.key == pygame.K_m:
            self.game_state = "menu"
            print("📋 Возврат в меню из паузы")
    
    def update(self):
        """Обновление игры с улучшенной обработкой"""
        try:
            # Обновляем задержку смены оружия
            if self.weapon_change_cooldown > 0:
                self.weapon_change_cooldown -= 1
            
            if self.game_state != "playing" and self.game_state != "paused":
                return
            
            # Обычное обновление игры
            self.player.update()
            self.spawn_enemy()
            self.particle_system.update()
            
            # Обновление тряски экрана
            if self.screen_shake > 0:
                self.screen_shake -= 1
            
            # Обновление врагов
            for enemy in self.enemies[:]:
                if enemy.update():
                    self.enemies.remove(enemy)
            
            # Обновление босса
            if self.boss:
                self.boss.update()
                if self.boss.health <= 0:
                    self.score += 500
                    self.level += 1
                    self.boss = None
                    self.particle_system.add_explosion(450, 300, (180, 0, 255), 100, 8)
            
            # Появление босса
            if not self.boss and self.score >= self.level * 100 and self.level % 2 == 1:
                self.boss = Boss()
            
            self.check_collisions()
            
        except Exception as e:
            print(f"💥 Ошибка в обновлении игры: {e}")
            traceback.print_exc()
    
    def draw_interface(self, surface):
        """Улучшенный интерфейс с информацией об оружии"""
        if self.game_state == "playing" or self.game_state == "paused":
            # Основная информация
            score_text = self.font_medium.render(f"Очки: {self.score}", True, WHITE)
            surface.blit(score_text, (10, 10))
            
            health_text = self.font_medium.render(f"Здоровье: {self.player.health}", True, GREEN)
            surface.blit(health_text, (10, 50))
            
            level_text = self.font_medium.render(f"Уровень: {self.level}", True, WHITE)
            surface.blit(level_text, (10, 90))
            
            # Информация об оружии
            weapon = mod_system.get_current_weapon()
            weapon_text = self.font_small.render(f"Оружие: {weapon['name']}", True, weapon['color'])
            surface.blit(weapon_text, (700, 10))
            
            # Подсказки управления
            controls_text = self.font_small.render("1-9: оружие, Q: след., P: пауза", True, GRAY)
            surface.blit(controls_text, (700, 40))
            
            # Если пауза
            if self.game_state == "paused":
                pause_text = self.font_large.render("ПАУЗА", True, YELLOW)
                surface.blit(pause_text, (450 - pause_text.get_width()//2, 200))
                continue_text = self.font_medium.render("Нажмите P для продолжения", True, WHITE)
                surface.blit(continue_text, (450 - continue_text.get_width()//2, 280))
            
            if self.boss:
                boss_text = self.font_medium.render("БОСС!", True, RED)
                surface.blit(boss_text, (450 - boss_text.get_width()//2, 10))

    def show_game_info(self):
        """Показ информации об игре"""
        print("\n" + "="*50)
        print("🐱 CAT WARRIOR ADVENTURE - ИНФОРМАЦИЯ")
        print("="*50)
        print("Управление:")
        print("  Меню: SPACE - игра, W - оружие, I - информация")
        print("  Игра: Стрелки - движение, SPACE - стрельба")
        print("         1-9 - оружие, Q - след. оружие, P - пауза")
        print("  Пауза: P - продолжить, ESC - меню")
        print(f"Доступно оружия: {len(mod_system.weapons)}")
        
        weapons = list(mod_system.weapons.items())
        for i, (name, data) in enumerate(weapons):
            print(f"  {i+1}. {data['name']} (Урон: {data['damage']})")
        print("="*50)

# Главная функция с улучшенной инициализацией
def main():
    print("🚀 Запуск Cat Warrior Adventure - Улучшенная версия")
    print("⏳ Инициализация...")
    
    try:
        # Проверка инициализации Pygame
        if not pygame.get_init():
            pygame.init()
        
        # Создание окна
        screen = pygame.display.set_mode((900, 600))
        pygame.display.set_caption("Cat Warrior Adventure - Стабильная версия")
        
        # Создание экземпляров
        mod_system = ModSystem()
        game = Game()
        
        print("✅ Игра успешно инициализирована!")
        print("🎮 Управление:")
        print("   Стрелки - движение, ПРОБЕЛ - стрельба")
        print("   1-9 - выбор оружия, Q - следующее оружие")
        print("   P - пауза, ESC - меню")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                game.handle_event(event)
            
            # Получаем состояние клавиш для плавного движения
            keys = pygame.key.get_pressed()
            if game.game_state == "playing":
                game.player.move(keys)
            
            # Обновление игры
            game.update()
            
            # Отрисовка
            game.draw()
            
            # Ограничение FPS
            clock.tick(60)
        
        pygame.quit()
        print("👋 Игра завершена")
        
    except Exception as e:
        print(f"💥 Критическая ошибка в главном цикле: {e}")
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
