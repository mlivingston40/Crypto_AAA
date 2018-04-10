

// This is for the menu dropdown displaying on hover rather than click

$('ul.nav li.dropdown').hover(function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(10).fadeIn(10);
}, function() {
  $(this).find('.dropdown-menu').stop(true, true).delay(10).fadeOut(10);
});
