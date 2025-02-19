
#### **Проект: "Светлячки"**

# Пояснительная записка

**Руководство пользователя** 
1. Запустите файл main.py.
2. В стартовом меню выберите "Играть" для начала игры, "Таблица рекордов" для просмотра лучших результатов или "Выход" для завершения программы.
3. Управляйте феей с помощью стрелок, клавиш WASD или мыши.
4. Собирайте светлячков, избегайте змей, ос и паутин.
5. Следите за светом феи: если он потухнет, игра завершится.
6. По окончании игры ваши результаты будут сохранены.

<figure>
  <figcaption>
    Главное меню
  </figcaption>
  <img src="./resource/screenshots/1.png" width="512"/>
</figure>

<figure>
  <figcaption>
    Уровень
  </figcaption>
  <img src="./resource/screenshots/2.png" width="512"/>
</figure>

**Руководство администратора**
1. Установите Python 3.x.
2. Установите библиотеки Pygame и Pillow с помощью команды
```
pip install -r requirements.txt
```
\
_Структура проекта:_ \
`main.py` — основной файл игры. \
`scores.csv` — файл для хранения результатов. \
`resources/` — папка со спрайтами.

### **1. Общее описание**

* **Название игры:** Светлячки
* **Цель игры:** Игрок управляет феей, собирая светлячков, чтобы зарабатывать очки и избегать ловушек. Если игрок слишком долго не ловит светлячков, его свет начинает гаснуть. Лес также ограничен "туманными облаками" на границе: если игрок пересекает границу, он получает предупреждение, и его свет начинает быстро тускнеть. Если он не вернется обратно в безопасную зону, игра заканчивается.
* **Целевая платформа:** ПК (Windows, Linux, MacOS)
* **Язык программирования:** Python
* **Библиотеки:** Pygame

### **2. Функциональные требования**

#### **2.1 Стартовое окно**

* Отображается заголовок игры ("Светлячки").
* Кнопки:
  + "Играть" — начинает игру.
  + "Таблица рекордов" — показывает лучшие результаты из файла scores.csv.
  + "Выход" — завершает игру.

#### **2.2 Финальное окно**

* Показывает результаты игры:
  + Количество собранных светлячков.
  + Время выживания.
  + Уровень сложности.
* Кнопки:
  + "Начать заново" — перезапускает игру.
  + "Выход" — завершает игру.

#### **2.3 Игровой процесс**

1. **Игрок (фея):**
   * Управление: стрелки, клавиши WASD или мышь.
   * Анимация: плавное движение, светящийся хвост.
   * Фея тускнеет, если долго не собирает светлячков.
2. **Светлячки (цель):**
   * Летают по экрану с случайной траекторией.
   * Анимация: мерцание и плавное движение.
   * Если фея сталкивается с ними, добавляются очки и восстанавливается её свет.
3. **Препятствия и враги:**
   * **Змеи:** двигаются по земле. Если фея касается змеи, игра заканчивается.
   * **Осы:** летают по экрану. Если оса сталкивается с феей, свет игрока уменьшается на 50%.
   * **Паутинки:** неподвижные объекты, если фея застревает, она теряет время (3 секунды), во время которого нельзя двигаться.
   * **Облака (граница):**
     + Расположены по краям игрового поля.
     + Если игрок вылетает за границу, он получает предупреждение.
     + Свет феи начинает быстро тускнеть, если она не возвращается в безопасную зону, игра заканчивается.
4. **Уровни сложности:**
   * С каждым уровнем:
     + Светлячки двигаются быстрее.
     + Появляется больше врагов и препятствий.
     + Хищники, такие как змеи и осы, становятся активнее.
   * Уровень отображается на экране.
5. **Механика света:**
   * Фея начинает гаснуть, если долго не ловить светлячков.
   * Если свет пропадает полностью, игра заканчивается.
6. **Очки и результаты:**
   * За каждого пойманного светлячка начисляются очки.
   * Счет отображается в реальном времени.
   * Финальные результаты записываются в scores.csv.

### **3. Нефункциональные требования**

* **requirements.txt**:
   Файл должен включать:
   pygame==2.x.x
* **Хранение данных:**
  + Очки записываются в scores.csv.
* **Кроссплатформенность:** Игра должна запускаться на всех операционных системах, где поддерживается Python.
* **Производительность:** Поддерживать стабильные 60 FPS.

### **4. Этапы разработки**

#### **4.1 Подготовка проекта**

* Настроить базовую структуру проекта.
* Создать стартовое окно.

#### **4.2 Реализация феи (игрока)**

* Добавить спрайт игрока.
* Настроить управление (клавиатура/мышь).
* Добавить анимацию (например, светящийся хвост).

#### **4.3 Реализация светлячков**

* Добавить спрайты светлячков.
* Настроить их случайное движение.
* Добавить анимацию мерцания.
* Реализовать столкновения с феей и подсчет очков.

#### **4.4 Препятствия и враги**

* **Змеи:**
  + Добавить спрайт змеи.
  + Настроить движение змеи вдоль земли.
  + Реализовать логику поражения при столкновении.
* **Осы:**
  + Добавить спрайт ос.
  + Настроить хаотичное движение по воздуху.
  + Реализовать уменьшение света при столкновении.
* **Паутинки:**
  + Добавить неподвижные спрайты паутин.
  + Реализовать задержку движения игрока при попадании в паутину.
* **Облака (граница):**
  + Создать полупрозрачные облака по краям игрового поля.
  + Добавить логику предупреждения и ускоренного гашения света при пересечении границы.

#### **4.5 Уровни сложности**

* Настроить систему уровней:
  + Увеличение скорости светлячков.
  + Появление новых препятствий и врагов.
* Отображение текущего уровня на экране.

#### **4.6 Финал и сохранение результатов**

* Создать финальное окно с результатами.
* Реализовать сохранение данных в scores.csv.
* Настроить загрузку таблицы рекордов.

### **5. Дизайн и анимация**

1. **Игровое поле:**
   * Фон: ночной лес (приглушенные темные цвета).
   * Атмосфера: лёгкий свет, исходящий от светлячков.
2. **Спрайты:**
   * **Фея:** небольшое яркое существо с мягкой анимацией движения.
   * **Светлячки:** разноцветные мерцающие точки.
   * **Препятствия:**
     + Змеи: тёмные, ползут по земле.
     + Осы: жёлто-чёрные, быстро движутся в воздухе.
     + Паутинки: полупрозрачные, стационарные.
     + Облака: полупрозрачные края экрана.
3. **Эффекты:**
   * Мерцание светлячков.
   * Гаснущий свет вокруг феи при низкой активности.
   * Световой след за феей.
