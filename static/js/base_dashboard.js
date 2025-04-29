/*************************************************
*  base_dashboard.js –  Dashboard SPA (v4.1)     *
*  • Loader משותף                               *
*  • סטייט ב-sessionStorage                     *
*  • currentPageID = מקור-אמת יחיד              *
**************************************************/



/* ─────────── 1. Consts ─────────── */
const ADMIN_DEFAULT = 'users_management';
const CLIENT_DEFAULT = 'cases_birds_view';

const userType   = document.getElementById('user-info').dataset.userType;

/* ─────────── 3. highlight ─────────── */
function highlightInSidebar(link, sidebar){
  document.querySelectorAll('.' + sidebar + ' a').forEach(a=>a.classList.remove('active'));
  link.classList.add('active');
}

/* ─────────── 4. Sub-menu ─────────── */
function showSubMenu(type, force=false){

  S.set(current_sub_sidebar, type);


  const cont = document.getElementById('subMenu');
  if(!cont) return;
  if(!force && cont.dataset.type===type) return;

  cont.dataset.type = type;

  let html='';
  if(type==='all_cases'){
    html=`
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="cases_birds_view" >מבט על תיקים</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="active_cases"     >תיקים פעילים</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="add_case"         >הוספת תיק</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="view_case"        >צפייה בתיק</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="archived_cases"   >ארכיון</a>`;
  }else if(type==='all_clients'){
    html=`
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="clients_birds_view" >מבט על לקוחות</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="active_clients"     >לקוחות פעילים</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="add_client"         >הוספת לקוח</a>
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="view_client"        >צפייה בלקוח</a>`;
  }else if(type==='attendancy'){
    html=`
      <a href="#" class="sub-sidebar-link" data-type="client" data-sidebar="sub-sidebar" data-page="attendancy_birds_view" >מבט על נוכחות</a>`;
  }
  cont.innerHTML = html;

  const pageNow = S.get(current_dashboard_content);
  if(pageNow){
    const link = cont.querySelector(`[data-page="${pageNow}"]`);
    if(link) highlightInSidebar(link, 'sub-sidebar');
  }
}


/* ─────────── 6. Startup ─────────── */
window.addEventListener('DOMContentLoaded',()=>{

  const targetPage = S.get(current_dashboard_content) || 
                     (userType==='admin' ? ADMIN_DEFAULT : CLIENT_DEFAULT);

  if(userType==='admin'){

    loadContent(page=targetPage, force=false, type='admin');

    /* highlight in sidebar */
    document.querySelectorAll('.sidebar a').forEach(a=>
      { 
        if(a.dataset.page===targetPage) {
          a.classList.add('active');
        }else{
          a.classList.remove('active');
        }
      
      }
    );

  }else if (userType==='client'){

    if (!S.get(current_sub_sidebar)){
      S.set(current_sub_sidebar, 'all_cases');
    }

    showSubMenu(type=S.get(current_sub_sidebar), force=true);
    loadContent(page=targetPage, force=false, type='client'); 

    /* highlight in sidebar */
    document.querySelectorAll('.sidebar a').forEach(a=>
      { 
        if(a.dataset.subSidebar===S.get(current_sub_sidebar)) {
          a.classList.add('active');
        }else{
          a.classList.remove('active');
        }
      
      }
    );
    
    /* highlight in sub sidebar */
    document.querySelectorAll('.sub-sidebar a').forEach(a=>
      { 
        if(a.dataset.page===targetPage) {
          a.classList.add('active');
        }else{
          a.classList.remove('active');
        }
      
      }
    );

  }


  /* ניווט דינמי – מאזין לכל הלחיצות */
  document.querySelector('.sidebar').addEventListener('click', (e) => {
    handle(e, sidebar_type=".sidebar");

  });

  if(userType==='client'){
    document.querySelector('.sub-sidebar').addEventListener('click', (e) => {
      handle(e, sidebar_class=".sub-sidebar");
    });
  }



  function handle(e, sidebar_class){
    
    const link = e.target.closest(sidebar_class + "-link");
    if (!link) return;
  
    const type = link.dataset.type;
    if (type) {

      if (type == 'admin'){
        const sidebar = link.dataset.sidebar;
        highlightInSidebar(link, sidebar);
        e.preventDefault();
        navigateTo(link, force=true);
        return;

      }else if (type == 'client'){

        const sidebar = link.dataset.sidebar;
        highlightInSidebar(link, sidebar);
        if (sidebar == 'sidebar') {
          showSubMenu(link.dataset.subSidebar);
        }else if (sidebar == 'sub-sidebar'){
          e.preventDefault();
          navigateTo(link, force=true);
          return;
        }


      }else{
        console.log("Error");
      }

    }
  }


});




/* ─────────── 8. Sidebar (mobile) ─────────── */
function toggleSidebar(){ 
  document.body.classList.toggle('sidebar-collapsed');
  document.querySelector('.sidebar').classList.toggle('collapsed');
  document.querySelector('.sub-sidebar').classList.toggle('collapsed');
}

/* ─────────── 9. Clock & Date ─────────── */
function updateDateTime(){
  const n=new Date();
  document.getElementById('current-date').textContent = n.toLocaleDateString('he-IL');
  document.getElementById('current-time').textContent = n.toLocaleTimeString('he-IL');
}
setInterval(updateDateTime,1000); updateDateTime();
