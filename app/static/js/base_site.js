/*************************************************
*          base_site.js  –  משתמש ב-Loader       *
**************************************************/
const DEFAULT_PAGE = 'home';  // ← שם יחיד ב-storage


/* אתחול */
window.addEventListener('DOMContentLoaded', () => {

  /* padding-top לפי גובה navbar */
  let dynamicContainer = document.getElementById('dynamicContent');
  const nav = document.querySelector('.navbar');
  if (nav) dynamicContainer.style.paddingTop = nav.offsetHeight + 'px';

  /* טעינה ראשונית */
  const pageSaved = S.get(current_site_content) || DEFAULT_PAGE;
  loadContent(
    page = pageSaved,
    force = true,
    type = "site"
  );

  /* ניווט דינמי – מאזין לכל הלחיצות */
  document.querySelector('.navbar').addEventListener('click', (e) => {
    const link = e.target.closest('.nav-link');
    if (!link) return;

    const page = link.dataset.page;
    if (page) {
      e.preventDefault();       // רק אם יש data-page — זה SPA
      navigateTo(link, force=true);
      return;
    }

    const clear = link.dataset.clear;
    if (clear) {
      e.preventDefault();
      clearStorageAndLogout(e);
      return;
    }

    // אחרת — אין page → נותנים לדפדפן להמשיך (למשל לוגאאוט רגיל)
  });
});

/* back / forward */
window.addEventListener('popstate', () => {
  const p = new URL(location.href).searchParams.get('page') || DEFAULT_PAGE;
  loadSiteContent(p, false);
});
