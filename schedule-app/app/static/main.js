

$(function() {
    let accountButton = $('#accountButton');
    let sidebar = $('.sidebar');
    let sidebarClose = $('.close');
    accountButton.click(function() {toggleSidebar(sidebar)});
    sidebarClose.click(function() {toggleSidebar(sidebar)});
});

function toggleSidebar(sidebar) {
    sidebar.animate({width:'toggle'},500);
    if (sidebar.hasClass('open'))
        sidebar.removeClass('open');
    else
        sidebar.addClass('open');
}