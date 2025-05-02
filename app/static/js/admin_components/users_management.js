/* static/js/admin_components/users_management.js */

window.init_users_management = function() {
  initUserForm();
};

window.initUserForm = function () {
  const form = document.getElementById('addUserForm');

  form.addEventListener('submit', async e => {
    e.preventDefault();
    
    const formData = new FormData(form);
    formData.append('action', 'add');

    const res = await fetch('/users_managment', { method: 'POST', body: formData });
    if (res.ok) {
      showToast("✅ המשתמש נוסף", "success");
      loadContent(page='users_management', force=true, type='admin');
    
    } else if (res.status === 409) {
      alert("⚠️ המשתמש כבר קיים");
    
    } else {
      alert("❌ שגיאה בהוספת המשתמש");
    }
  });
};

/* איפוס סיסמה */
window.updateUser = function (event, username) {
  event.preventDefault();
  const formData = new FormData(event.target);
  formData.append('action', 'update');
  formData.append('username', username);

  fetch('/users_managment', { method: 'POST', body: formData })
    .then(r => {
      if (r.ok) {
        showToast("✅ הסיסמה עודכנה", "success");
        loadContent(page='users_management', force=true, type='admin');
      
      } else alert("❌ שגיאה בעדכון");
    });
};

/* מחיקה */
window.deleteUser = function (username) {
  if (!confirm(`למחוק את המשתמש “${username}”?`)) return;
  const fd = new FormData();
  fd.append('action', 'delete');
  fd.append('username', username);

  fetch('/users_managment', { method: 'POST', body: fd })
    .then(r => {
      if (r.ok) {
        showToast("✅ המשתמש נמחק", "success");
        loadContent(page='users_management', force=true, type='admin');
      
      } else alert("❌ שגיאה במחיקה");
    });
};

/* במקרה שה-HTML הוצג כחלק מדף מלא ולא דרך loadDynamicContent */
document.addEventListener('DOMContentLoaded', () => initUserForm());
