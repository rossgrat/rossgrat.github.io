const siteHeader = document.querySelector('.site-header');
new ResizeObserver(() => {
    document.documentElement.style.setProperty('--header-height', `${siteHeader.getBoundingClientRect().height}px`);
}).observe(siteHeader);

const postContents = document.querySelector('.post-toc details');
if (postContents) {
    const desktop = window.matchMedia('(min-width: 1200px)');
    const updateContents = () => { postContents.open = desktop.matches; };
    updateContents();
    desktop.addEventListener('change', updateContents);
    postContents.addEventListener('click', (event) => {
        if (!desktop.matches && event.target.closest('a')) postContents.open = false;
    });
}
