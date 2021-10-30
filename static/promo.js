// Скрипт подгрузился, взяли текущую цену из конструктора торта
const priceFromConstructor = Number.parseInt(
    document.querySelector('#total_price').textContent
);

// Собираем в DOM нужные элементы
const currentPriceDisplay = document.querySelector('#total_price');
const deliveryDateTimeInput = document.querySelector('#id_order_datetime');
const userPromoCodeInput = document.querySelector('#promo');
const userPromoCodeHiddenInput = document.querySelector('#promo_code');
const promoCodeCheckingResult = document.querySelector('#promocode_checking');
const totalPriceHiddenInput = document.querySelector('#price');
const orderForm = document.querySelector('.form-group');

/*
Логика подсчета итоговой цены
*/
// Вводим переменные для коэффициента срочности и коэффициента промокода
let urgencyRate = 0;
let promoCodeRate = 0;
// Функция для подсчета цены
const getTotalPrice = () => priceFromConstructor * (
    1 - promoCodeRate + urgencyRate
);

/*
Логика изменения цены в зависимости от промокода
*/
const changePriceDueToUrgency = () => {
    const startTime = Date.now();
    const endTime = Date.parse(deliveryDateTimeInput.value);
    const interval = (endTime - startTime) / 3600000;
    const notification = document.querySelector('#raise_price_notification');
    if (interval < 5) {
        console.log('Находимся в интервале до 5 часов');
        console.log(interval);
        urgencyRate = 0;
        notification.innerHTML = '<span style="color: red;">Время доставки меньше 5 часов, так быстро только пирожков можно напечь</span>';
    }
    if (interval >= 5 && interval < 24) {
        console.log('Находимся в интервале от 5 до 24 часов');
        console.log(interval);
        urgencyRate = 0.2;
        notification.innerHTML = 'Доставка в пределах 24 часов увеличивает цену на 20%';
    }
    if (interval >= 24) {
        console.log('Находимся в интервале свыше 24 часов');
        console.log(interval);
        urgencyRate = 0;
        notification.innerHTML = '';
    }
    currentPriceDisplay.innerHTML = `${getTotalPrice()} &#8381;`;
}

/*
Логика изменения цены в зависимости от промокода
*/

// список для хранения полученных с сервера данных о промокоде
// с этими данными будут сравниваться инпуты юзера
const promoCodeStatus = [];
// функция для запроса к API, ответ распиливается и помещается в список promoCodeStatus
const getPromoCodeStatus = () => {
    const makeRequest = async() => {
        const response = await fetch('http://localhost:8000/get_code');
        const { actualCode, thisClientUsed } = await response.json();
        promoCodeStatus.push(actualCode, thisClientUsed);
    }
    makeRequest();
}

// запрашиваем с сервера данные об актуальном промокоде
getPromoCodeStatus();

const userPromoCodeInputHandler = () => {
        const userInput = document.querySelector('#promo').value;
        // распиливаем полученные от сервера данные
        const [actualCode, thisClientUsed] = promoCodeStatus;
        if (userInput === actualCode) {
            if (thisClientUsed) {
                promoCodeCheckingResult.classList.add('text-danger');
                promoCodeCheckingResult.innerHTML = 'Вы уже использовали этот промокод.';
            } else {
                // если промик верный и используют впервые отключаем инпут, он уже незачем
                userPromoCodeInput.disabled = true;
                promoCodeCheckingResult.classList.add('text-success');
                promoCodeCheckingResult.classList.remove('text-danger');
                promoCodeCheckingResult.innerHTML = 'Ура! Промокод верный! Ваша скидка &mdash; 20%.\nСтоимость заказа пересчитана.';
                userPromoCodeHiddenInput.value = actualCode;
                // Обновляем коэффициент цены с промокодом
                promoCodeRate = 0.2;
                // Выводим цену с учетом промика и срочности заказа
                currentPriceDisplay.innerHTML = `${getTotalPrice()} &#8381;`;
            }
        } else if (userInput.length > 0) {
            promoCodeCheckingResult.innerHTML = 'К сожалению, у нас нет такого промокода.';
            promoCodeCheckingResult.classList.remove('text-success');
            promoCodeCheckingResult.classList.add('text-danger');
        } else {
            promoCodeCheckingResult.innerHTML = '';
        }
    }


/* Вешаем слушателей */

// Повесили слушателя события инпута в поле с датой и временем
deliveryDateTimeInput.addEventListener(
    'input',
    changePriceDueToUrgency
)

// Повесили слушателя события инпута в поле для ввода промика
userPromoCodeInput.addEventListener(
    'keyup',
    userPromoCodeInputHandler
)

// Повесли слушателя на сабмит формы, чтобы он пробросил в скрытый инпут итоговую цену
orderForm.addEventListener(
    'submit',
    () => {
        totalPriceHiddenInput.value = getTotalPrice();
    }
)
