document.addEventListener('DOMContentLoaded', function () {
    const filterBtn = document.getElementById('filterBtn');
    const filterPanel = document.getElementById('filterPanel');
    const closeFilter = document.getElementById('closeFilter');

    if (!filterBtn || !filterPanel) return;

    const toggleFilter = () => {
        const isHidden = filterPanel.classList.toggle('hidden');
        filterBtn.setAttribute('aria-expanded', !isHidden);
    };

    filterBtn.addEventListener('click', (e) => {
        e.preventDefault();
        toggleFilter();
    });

    closeFilter?.addEventListener('click', (e) => {
        e.preventDefault();
        filterPanel.classList.add('hidden');
        filterBtn.setAttribute('aria-expanded', 'false');
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
        if (!filterBtn.contains(e.target) && !filterPanel.contains(e.target)) {
            filterPanel.classList.add('hidden');
            filterBtn.setAttribute('aria-expanded', 'false');
        }
    });

    // Keyboard support
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !filterPanel.classList.contains('hidden')) {
            filterPanel.classList.add('hidden');
            filterBtn.setAttribute('aria-expanded', 'false');
        }
    });
});