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
  
/*PUBLIC*/
window.addEventListener('load', function() {
    __set_event_click_for_info()
})
