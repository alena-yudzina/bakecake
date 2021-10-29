const userPromoCodeInput = document.querySelector('#promo');
const userPromoCodeHiddenInput = document.querySelector('#promo_code');
const promoCodeCheckingResult = document.querySelector('#promocode_checking');
const currentPrice = document.querySelector('#total_price');
const currentPriceInput = document.querySelector('#price');
const deliveryDateTime = document.querySelector('#id_order_datetime');
const promoCodeStatus = [];


const getPromoCodeStatus = () => {
    const makeRequest = async() => {
        const response = await fetch('http://localhost:8000/get_code');
        const { actualCode, thisClientUsed } = await response.json();
        promoCodeStatus.push(actualCode, thisClientUsed);
    }
    makeRequest();
}

const userPromoCodeInputHandler = () => {
        const userInput = document.querySelector('#promo').value;
        const [actualCode, thisClientUsed] = promoCodeStatus;
        if (userInput === actualCode) {
            if (thisClientUsed) {
                promoCodeCheckingResult.classList.add('text-danger');
                promoCodeCheckingResult.innerHTML = 'Вы уже использовали этот промокод.';
                userPromoCodeHiddenInput.value = null;
            } else {
                userPromoCodeInput.disabled = true;
                promoCodeCheckingResult.classList.add('text-success');
                promoCodeCheckingResult.classList.remove('text-danger');
                promoCodeCheckingResult.innerHTML = 'Ура! Промокод верный! Ваша скидка &mdash; 20%.\nСтоимость заказа пересчитана.';
                const price = Number.parseInt(currentPrice.textContent) * 0.8;
                currentPrice.innerHTML = `${price} &#8381;`;
                currentPriceInput.value = price;
                userPromoCodeHiddenInput.value = actualCode;
            }
        } else if (userInput.length > 0) {
            promoCodeCheckingResult.innerHTML = 'К сожалению, у нас нет такого промокода.';
            promoCodeCheckingResult.classList.remove('text-success');
            promoCodeCheckingResult.classList.add('text-danger');
        } else {
            promoCodeCheckingResult.innerHTML = '';
    }
}

getPromoCodeStatus();
currentPriceInput.value = Number.parseInt(currentPrice.textContent);

userPromoCodeInput.addEventListener(
    'keyup',
    userPromoCodeInputHandler
)

let priceIsRaised = false;

deliveryDateTime.addEventListener(
    'input',
    () => {
        const startTime = Date.now();
        const endTime = Date.parse(deliveryDateTime.value);
        const interval = (endTime - startTime) / 3600000;
        const notification = document.querySelector('#raise_price_notification');
        console.log(interval);
        if (interval < 5) {
            notification.innerHTML = '<span style="color: red;">Время доставки меньше 5 часов, так быстро только пирожков можно напечь</span>';
        }
        if (5 <= interval < 24 && !priceIsRaised) {
            const price = Math.round(
                Number.parseInt(currentPrice.textContent) * 1.2
            )
            currentPrice.innerHTML = `${price} &#8381;`;
            currentPriceInput.value = price;
            priceIsRaised = true;
            notification.innerHTML = 'Доставка в пределах 24 часов увеличивает цену на 20%';
        }
        if (interval >= 24 && priceIsRaised) {
            const price = Math.round(
                Number.parseInt(currentPrice.textContent) / 1.2
            )
            currentPrice.innerHTML = `${price} &#8381;`;
            currentPriceInput.value = price;
            priceIsRaised = false;
            notification.innerHTML = '';
        }
        console.log(currentPriceInput.value);
    }
)
