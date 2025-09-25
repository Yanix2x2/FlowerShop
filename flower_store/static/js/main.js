// Находим все элементы на странице
const boxes = document.querySelectorAll('.box');
const showMoreButton = document.getElementById('showMoreButton');

// Настройки
let itemsToShow = 6; // Сколько элементов показывать за раз
let currentIndex = itemsToShow; // С какого элемента начинать (первые 6 уже видны)

// Функция для первоначального скрытия элементов
function hideBoxesOnLoad() {
  // Проходим по всем боксам, начиная с 6-го (индекс 5) и скрываем их
  for (let i = currentIndex; i < boxes.length; i++) {
    boxes[i].classList.add('hidden');
  }

  // Проверяем, нужно ли вообще показывать кнопку
  // Если элементов 6 или меньше, кнопка будет сразу скрыта
  checkButtonVisibility();
}

// Функция, которая вызывается при нажатии на кнопку
function showMoreItems() {
  // Показываем следующие 6 элементов (или меньше, если осталось мало)
  let nextIndex = currentIndex + itemsToShow;

  for (let i = currentIndex; i < nextIndex && i < boxes.length; i++) {
    boxes[i].classList.remove('hidden');
  }

  // Обновляем индекс, с которого начнём в следующий раз
  currentIndex = nextIndex;

  // Проверяем, не пора ли скрыть кнопку
  checkButtonVisibility();
}

// Функция для проверки, нужно ли скрыть кнопку
function checkButtonVisibility() {
  // Если текущий индекс >= общего количества элементов, значит, все показаны
  if (currentIndex >= boxes.length) {
    showMoreButton.style.display = 'none'; // Скрываем кнопку
  }
}

// Вешаем обработчик события на кнопку
showMoreButton.addEventListener('click', showMoreItems);

// Вызываем функцию при загрузке страницы, чтобы скрыть лишние элементы
hideBoxesOnLoad();