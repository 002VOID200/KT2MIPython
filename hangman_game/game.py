import random
import os
import sys

def clear_console():
    """Очистка консоли"""
    if sys.platform.startswith('win'):
        os.system('cls')
    else:
        os.system('clear')

def load_words(filename):
    """Загрузка слов из файла"""
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(',')
                    word = parts[0].strip().lower()
                    description = parts[1].strip() if len(parts) > 1 else "Нет описания"
                    hint = parts[2].strip() if len(parts) > 2 else ""
                    words.append({
                        'word': word,
                        'description': description,
                        'hint': hint
                    })
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден!")
        input("Нажми Enter для выхода...")
        sys.exit(1)
    return words

def load_gallows_stage(stage):
    """Загрузка фрагмента виселицы"""
    try:
        with open(f'gallows{stage}.txt', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"[Ошибка: не найден файл gallows{stage}.txt]"

def display_word(word, guessed_letters):
    """Отображение слова с угаданными буквами"""
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

def play_game():
    """Основная логика игры"""
    # Загружаем слова
    words = load_words('words.txt')
    if not words:
        print("Нет доступных слов для игры!")
        return
    
    # Выбираем случайное слово
    word_data = random.choice(words)
    word = word_data['word']
    description = word_data['description']
    hint = word_data['hint']
    
    guessed_letters = set()
    wrong_letters = set()
    errors = 0
    max_errors = 7
    
    clear_console()
    print("=" * 60)
    print("🎯 Добро пожаловать в 'ВИСЕЛИЦА НА ПОЛЕ ЧУДЕС'!")
    print("=" * 60)
    print(f"📖 Описание: {description}")
    if hint:
        print(f"💡 Подсказка: {hint}")
    print(f"🔤 В слове {len(word)} букв.")
    print("=" * 60)
    input("Нажми Enter чтобы начать...")
    
    while errors < max_errors:
        clear_console()
        
        # Показываем текущее состояние
        print(load_gallows_stage(errors))
        print(f"\n📝 Слово: {display_word(word, guessed_letters)}")
        print(f"❌ Неправильные буквы: {', '.join(sorted(wrong_letters)) if wrong_letters else 'нет'}")
        print(f"❤️ Осталось попыток: {max_errors - errors}")
        print("-" * 40)
        
        # Проверка на победу
        if all(letter in guessed_letters for letter in word):
            clear_console()
            print(load_gallows_stage(errors))
            print(f"\n🎉🎉🎉 ПОБЕДА! 🎉🎉🎉")
            print(f"✨ Вы угадали слово: {word.upper()}")
            print(f"✨ Осталось жизней: {max_errors - errors}")
            break
        
        # Ввод буквы
        letter = input("🔠 Введите букву: ").strip().lower()
        
        # Проверка ввода
        if not letter or len(letter) != 1:
            print("⚠️ Введите одну букву!")
            input("Нажми Enter чтобы продолжить...")
            continue
        
        if not letter.isalpha():
            print("⚠️ Введите букву русского алфавита!")
            input("Нажми Enter чтобы продолжить...")
            continue
        
        # Проверка, не называли ли уже эту букву
        if letter in guessed_letters or letter in wrong_letters:
            print("⚠️ Вы уже называли эту букву!")
            input("Нажми Enter чтобы продолжить...")
            continue
        
        # Проверка, есть ли буква в слове
        if letter in word:
            guessed_letters.add(letter)
            print("✅ Правильно!")
        else:
            wrong_letters.add(letter)
            errors += 1
            print(f"❌ Неправильно! Буквы '{letter}' нет в слове.")
        
        input("Нажми Enter чтобы продолжить...")
    
    # Если проиграли
    if errors >= max_errors:
        clear_console()
        print(load_gallows_stage(max_errors))
        print(f"\n💀💀💀 ВЫ ПРОИГРАЛИ! 💀💀💀")
        print(f"📖 Загаданное слово: {word.upper()}")
    
    print("\n" + "=" * 60)

def main():
    """Главная функция"""
    while True:
        play_game()
        again = input("\n🔄 Хотите сыграть ещё раз? (да/нет): ").strip().lower()
        if again not in ['да', 'yes', 'д', 'y', 'конечно', '+']:
            print("\n👋 Спасибо за игру! До свидания!")
            break

if __name__ == "__main__":
    main()