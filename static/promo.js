const userPromoCodeInput = document.querySelector('#promo');
const promoCodeCheckingResult = document.querySelector('#promocode_checking')
const currentPrice = document.querySelector('#id_price')
const promoCode = '12345'


const promoCodeIsUsed = async code => {
    // На дальнейшую доработку: требуется проверка статусов ответа
    const response = await fetch(`http://localhost:8000/check_code/${code}`);
    const {codeIsUsed} = await response.json();
    return codeIsUsed;
}

userPromoCodeInput.addEventListener(
    'keyup',
    async function () {
        const userInput = document.querySelector('#promo').value;
        if (userInput === promoCode) {
            const codeIsUsed = await promoCodeIsUsed(promoCode);
            if (codeIsUsed) {
                promoCodeCheckingResult.classList.add('text-danger');
                promoCodeCheckingResult.innerHTML = 'Вы уже использовали этот промокод.';
            } else {
                userPromoCodeInput.disabled = true;
                promoCodeCheckingResult.classList.add('text-success');
                promoCodeCheckingResult.classList.remove('text-danger');
                promoCodeCheckingResult.innerHTML = 'Ура! Промокод верный! Ваша скидка &mdash; 20%.\nСтоимость заказа пересчитана.';
                currentPrice.value = Number.parseInt(currentPrice.value) * 0.8;
            }
        } else if (userInput.length > 0) {
            promoCodeCheckingResult.innerHTML = 'К сожалению, у нас нет такого промокода.';
            promoCodeCheckingResult.classList.remove('text-success');
            promoCodeCheckingResult.classList.add('text-danger');
        } else {
            promoCodeCheckingResult.innerHTML = '';
        }
    }
)
