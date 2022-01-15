'use strict';

{
    console.log(`from js : ${drinkingId}`);

    var activeDrinkId = 'drink_' + drinkingId;

    const activeDrink = document.getElementById(activeDrinkId);
    activeDrink.classList.add('border-danger', 'shadow', 'mb-3');

    const activeDrinkTime = activeDrink.querySelector('.invisible');
    activeDrinkTime.classList.remove('invisible');

}