'use strict';

{
    console.log(`from js : ${drinkingId}`);
    
    // セッションから取得したIDを加工
    var activeDrinkId = 'drink_' + drinkingId;
    
    // 該当IDを目立たせる
    const activeDrink = document.getElementById(activeDrinkId);

    if (activeDrink) {
        activeDrink.classList.add('border-danger', 'shadow', 'mb-3');
        
        // 非表示要素を表示させる
        const activeDrinkTime = activeDrink.querySelector('.d-none');
        activeDrinkTime.classList.remove('d-none');
    }
    

    // セッションから取得したIDを加工
    var editDrinkId = 'edit_drink_' + drinkingId;
    
    // 該当IDを取得
    const editDrinkH1 = document.getElementById(editDrinkId);
    
    if (editDrinkH1) {
        // 飲酒中テキストを表示
        editDrinkH1.innerHTML += '(飲酒中)';

        // 非表示要素を表示させる
        const finishDrinkButton = document.querySelector('.invisible');
        finishDrinkButton.classList.remove('invisible');
    }
    
    
    
}