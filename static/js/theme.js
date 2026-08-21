function setTheme(theme) {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('paintHubTheme', theme);

    document.querySelectorAll('[data-theme-option]').forEach((button) => {
        button.classList.toggle('is-active', button.dataset.themeOption === theme);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const currentTheme = document.documentElement.dataset.theme || 'light';
    setTheme(currentTheme);

    document.querySelectorAll('[data-theme-option]').forEach((button) => {
        button.addEventListener('click', () => {
            setTheme(button.dataset.themeOption);
        });
    });
});
