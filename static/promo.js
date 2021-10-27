const userPromoCodeInput = document.querySelector('#promo');
const promoCodeCheckingResult = document.querySelector('#promocode_checking')
const currentPrice = document.querySelector('#id_price')
const promoCode = '12345'

userPromoCodeInput.addEventListener(
    'keyup',
    () => {
        const userInput = document.querySelector('#promo').value;
        if (userInput === promoCode) {
            userPromoCodeInput.disabled = true;
            promoCodeCheckingResult.classList.add('text-success');
            promoCodeCheckingResult.classList.remove('text-danger');
            promoCodeCheckingResult.innerHTML = 'Ура! Промокод верный! Ваша скидка &mdash; 20%.\nСтоимость заказа пересчитана.'
            currentPrice.value = Number.parseInt(currentPrice.value) * 0.8
        } else if (userInput.length > 0) {
            promoCodeCheckingResult.innerHTML = 'К сожалению, у нас нет такого промокода.';
            promoCodeCheckingResult.classList.remove('text-success');
            promoCodeCheckingResult.classList.add('text-danger');
        } else {
            promoCodeCheckingResult.innerHTML = '';
        }
    }
)
