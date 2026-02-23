import os
import json
import sys

def install_all_mods():
    """Устанавливает все моды в папку игры"""
    
    print("🐱 Установка модов для Cat Warrior Adventure")
    print("=" * 50)
    
    # Определяем где мы находимся
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Текущая папка: {current_dir}")
    
    # Варианты путей к папке с игрой
    possible_paths = [
        "CatWarriorAdventure_Complete",  # Если скрипт рядом с игрой
        os.path.join(current_dir, "CatWarriorAdventure_Complete"),  # Абсолютный путь
        "..",  # На уровень выше
        os.path.dirname(current_dir)  # Родительская папка
    ]
    
    game_folder = None
    for path in possible_paths:
        if os.path.exists(path) and any(os.path.exists(os.path.join(path, f)) for f in ["cat_warrior_adventure.py", "CatWarriorAdventure_Complete.exe"]):
            game_folder = path
            print(f"✅ Найдена папка игры: {game_folder}")
            break
    
    if not game_folder:
        print("❌ Папка игры не найдена!")
        print("Убедитесь, что:")
        print("1. Игра уже запускалась хотя бы раз")
        print("2. Этот файл находится в той же папке, что и игра")
        print("3. Или создайте папку вручную")
        
        # Спросим пользователя
        user_input = input("Введите путь к папке игры (или нажмите Enter для автосоздания): ").strip()
        if user_input:
            game_folder = user_input
        else:
            game_folder = "CatWarriorAdventure_Complete"
            print(f"Создаем папку: {game_folder}")
    
    # Создаем структуру папок если нужно
    folders_to_create = [
        os.path.join(game_folder, "Mods", "Cats"),
        os.path.join(game_folder, "Mods", "Levels"), 
        os.path.join(game_folder, "Mods", "Weapons")
    ]
    
    for folder in folders_to_create:
        os.makedirs(folder, exist_ok=True)
        print(f"📁 Создана папка: {folder}")
    
    # Данные модов (те же что и раньше)
    mods_data = {
        "Cats": [
            {
                "file": "god_cat.json",
                "content": {
                    "name": "💫 БОЖЕСТВЕННЫЙ КОТ",
                    "description": "Непобедимый кот с божественными способностями!",
                    "author": "CatModder",
                    "version": "2.0",
                    "speed": 15,
                    "health": 9999,
                    "color": [255, 215, 0]
                }
            },
            {
                "file": "night_hunter.json", 
                "content": {
                    "name": "🌙 НОЧНОЙ ОХОТНИК",
                    "description": "Страж ночи - невидим для врагов ночью",
                    "author": "ShadowDeveloper",
                    "version": "1.5",
                    "speed": 8,
                    "health": 120,
                    "color": [30, 30, 60]
                }
            }
        ],
        "Levels": [
            {
                "file": "space_level.json",
                "content": {
                    "name": "🚀 КОСМИЧЕСКИЙ УРОВЕНЬ", 
                    "description": "Сражение среди звезд с инопланетными врагами!",
                    "author": "SpaceDesigner",
                    "version": "1.8",
                    "enemy_spawn_rate": 45,
                    "enemy_health_multiplier": 1.8
                }
            }
        ],
        "Weapons": [
            {
                "file": "death_cannon.json",
                "content": {
                    "name": "💥 ПУШКА СМЕРТИ",
                    "description": "Оружие массового поражения!",
                    "author": "WeaponMaster", 
                    "version": "3.0",
                    "shoot_cooldown": 60,
                    "damage_multiplier": 10.0
                }
            }
        ]
    }
    
    installed_count = 0
    
    for category, mods in mods_data.items():
        category_folder = os.path.join(game_folder, "Mods", category)
        
        for mod in mods:
            file_path = os.path.join(category_folder, mod["file"])
            
            # Сохраняем мод в файл
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(mod["content"], f, indent=4, ensure_ascii=False)
            
            print(f"✅ Установлен мод: {mod['content']['name']}")
            installed_count += 1
    
    print(f"\n🎮 Установлено модов: {installed_count}")
    print("💫 Перезапустите игру чтобы увидеть новые моды!")
    
    # Покажем где искать моды в игре
    print("\n📋 Как использовать моды в игре:")
    print("1. Запустите игру")
    print("2. Нажмите M для входа в меню модов") 
    print("3. Выберите категорию (Коты/Уровни/Оружие)")
    print("4. Нажмите цифру соответствующую моду")
    print("5. Начните новую игру!")
    
    input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    install_all_mods()
