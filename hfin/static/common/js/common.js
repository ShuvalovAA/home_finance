function __set_event_click_for_info(){
    info_buttons = document.getElementsByName('info')
    for( i=0; i < info_buttons.length; i++){
        el = info_buttons[i]
        el.addEventListener(
            'click',
            function(e){
                button_info = document.getElementById('info')
                button_info.click()
            }
        )
    }
}


function get_russian_inflation(){
    var country = 'Russia'
    $.ajax({
        method: 'GET',
        url: 'https://api.api-ninjas.com/v1/inflation?country=' + country,
        headers: { 'X-Api-Key': 'quHHBru6EJ6N+dBiL/cmCQ==eMqzk4Tp3TKJCjG0'},
        contentType: 'application/json',
        success: function(result) {
            console.log(result);
        },
        error: function ajaxError(jqXHR) {
            console.error('Error: ', jqXHR.responseText);
        }
    });
}
  
/*PUBLIC*/
window.addEventListener('load', function() {
    __set_event_click_for_info()
})
