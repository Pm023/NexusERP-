/**
 * NexusERP Theme Engine - Handles Dark/Light Mode
 */

(function () {
    // Immediately invoke to prevent flash of light theme
    const savedTheme = localStorage.getItem('nexus-theme');
    const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');
    
    document.documentElement.setAttribute('data-theme', initialTheme);

    // Initialize toggle when DOM is ready
    document.addEventListener('DOMContentLoaded', function () {
        setupThemeToggle();
    });

    window.setupThemeToggle = function () {
        const toggleCheckbox = document.getElementById('themeCheckbox');
        if (!toggleCheckbox) return;

        // Sync toggle check status
        const currentTheme = document.documentElement.getAttribute('data-theme');
        toggleCheckbox.checked = (currentTheme === 'dark');

        // Toggle listener
        toggleCheckbox.addEventListener('change', function () {
            const newTheme = toggleCheckbox.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('nexus-theme', newTheme);
            
            // Dispatch custom event for charts if they need to refresh colors
            window.dispatchEvent(new CustomEvent('themeChanged', { detail: newTheme }));
        });
    };
})();
