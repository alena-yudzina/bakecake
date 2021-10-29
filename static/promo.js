const userPromoCodeInput = document.querySelector('#promo');
const userPromoCodeHiddenInput = document.querySelector('#promo_code');
const promoCodeCheckingResult = document.querySelector('#promocode_checking');
const currentPrice = document.querySelector('#total_price');
const currentPriceInput = document.querySelector('#price');
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
                currentPrice.textContent = Number.parseInt(currentPrice.textContent) * 0.8;
                currentPriceInput.value = currentPrice.textContent;
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
