# Папка для основной логики
# Здесь будет находиться ядро программы (backend), которое взаимодействует с системными менеджерами пакетов.

import subprocess
import json
from typing import List, Dict, Any

class PackageManager:
    """
    Класс для унифицированного взаимодействия со всеми пакетными менеджерами.
    """

    def get_pacman_packages(self) -> List[Dict[str, str]]:
        """
        Получает список установленных пакетов через pacman.
        Возвращает список словарей: [{"name": "pkgA", "version": "1.0", ...}, ...]
        """
        print("--- Получение данных из Pacman ---")
        try:
            # Используем pacquery или аналогичный метод для получения структурированных данных, 
            # но пока используем простой список, чтобы избежать сложных зависимостей.
            result = subprocess.run(
                ['pacman', '-Q', 'installed'], 
                capture_output=True, text=True, check=True
            )
            
            packages = []
            lines = result.stdout.strip().split()
            # Простой парсинг: name version ...
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    name = lines[i]
                    version = lines[i+1]
                    packages.append({"source": "pacman", "name": name, "version": version})
            return packages

        except subprocess.CalledProcessError as e:
            print(f"Ошибка при вызове pacman: {e}")
            return []
        except FileNotFoundError:
            print("Ошибка: Команда 'pacman' не найдена. Возможно, работаем не на Arch-подобной системе.")
            return []

    def get_flatpak_packages(self) -> List[Dict[str, str]]:
        """
        Получает список установленных пакетов через Flatpak.
        """
        print("--- Получение данных из Flatpak ---")
        try:
            # flatpak list --app (или другой подходящий вывод для парсинга)
            result = subprocess.run(
                ['flatpak', 'list', '--columns=application,name,version'], 
                capture_output=True, text=True, check=True
            )

            packages = []
            lines = result.stdout.strip().split('\n')
            # Пропускаем заголовок
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 3:
                    app_id = parts[0] # Пример: org.kde.kactivitymanagerd
                    name = parts[1]
                    version = parts[2]
                    packages.append({"source": "flatpak", "application_id": app_id, "name": name, "version": version})
            return packages

        except subprocess.CalledProcessError as e:
            print(f"Ошибка при вызове flatpak: {e}")
            # Flatpak может не быть установлен или иметь другую команду вывода
            return []
        except FileNotFoundError:
            print("Ошибка: Команда 'flatpak' не найдена.")
            return []


    def get_all_packages(self) -> List[Dict[str, str]]:
        """
        Собирает список пакетов из всех доступных источников.
        """
        print("\n======================================")
        print("Начинается сбор данных о пакетах...")
        
        # 1. Pacman
        pac_packages = self.get_pacman_packages()
        # 2. Flatpak
        flatpak_packages = self.get_flatpak_packages()

        all_packages = pac_packages + flatpak_packages
        
        print(f"\n✅ Данные собраны!")
        print(f"   - Pacman: {len(pac_packages)} пакетов")
        print(f"   - Flatpak: {len(flatpak_packages)} приложений")

        return all_packages

if __name__ == "__main__":
    # Проверка работы ядра
    manager = PackageManager()
    installed_packages = manager.get_all_packages()
    
    print("\n--- Примеры полученных данных ---")
    for i, pkg in enumerate(installed_packages[:5]):
        print(f"[{i+1}] Source: {pkg['source'].upper()}, Name: {pkg['name']}, Version: {pkg.get('version', 'N/A')}")

