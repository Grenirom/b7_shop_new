window.addEventListener('load', function () {
    var savedTheme = localStorage.getItem('jazzmin_theme');
    var savedStickyActions = localStorage.getItem('jazzmin_sticky_actions');

    if (savedTheme) {
        document.body.classList.add('theme-' + savedTheme);
    }
    if (savedStickyActions) {
        document.body.classList.toggle('sticky-actions', savedStickyActions === 'true');
    }

    document.body.addEventListener('themechange', function (event) {
        localStorage.setItem('jazzmin_theme', event.detail.theme);
    });
    document.body.addEventListener('stickyactionschange', function (event) {
        localStorage.setItem('jazzmin_sticky_actions', event.detail.stickyActions);
    });
});