$(function() {
    let accountButton = $('#accountButton');
    let sidebar = $('.sidebar');
    let sidebarClose = $('.close');
    let sidebarError = $('.sidebarError');
    accountButton.click(function() {toggleSidebar(sidebar)});
    sidebarClose.click(function() {toggleSidebar(sidebar)});
    if(sidebarError.children().length > 0)
        sidebar.addClass('open');
});

function toggleSidebar(sidebar) {
    sidebar.animate({width:'toggle'},500);
    if (sidebar.hasClass('open'))
        sidebar.removeClass('open');
    else
        sidebar.addClass('open');
}

function setCookie(name,val,exp) {
    let expires = '';
    if (exp) {
        let date = new Date();
        date.setTime(date.getTime() + (exp*24*60*60*1000));
        expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (val || '')  + expires + '; path=/';
}
function getCookie(name) {
    let nameEQ = name + '=';
    let ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}
function eraseCookie(name) {
    document.cookie = name+'=; Max-Age=-99999999;';
}