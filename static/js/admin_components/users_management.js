/* static/js/admin_components/user_management.js */

window.initUserForm = function () {
  const form = document.getElementById('addUserForm');
  if (form) {
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const formData = new FormData(form);
      formData.append('action', 'add');

      const res = await fetch('/user_managment', { method: 'POST', body: formData });
      if (res.ok) {
        showToast("✅ המשתמש נוסף");
        loadDynamicContent('/load_user_management');
      } else if (res.status === 409) {
        alert("⚠️ המשתמש כבר קיים");
      } else {
        alert("❌ שגיאה בהוספת המשתמש");
      }
    });
  }
};

/* איפוס סיסמה */
window.updateUser = function (event, username) {
  event.preventDefault();
  const formData = new FormData(event.target);
  formData.append('action', 'update');
  formData.append('username', username);

  fetch('/user_managment', { method: 'POST', body: formData })
    .then(r => {
      if (r.ok) {
        showToast("✅ הסיסמה עודכנה");
        loadDynamicContent('/load_user_management');
      } else alert("❌ שגיאה בעדכון");
    });
};

/* מחיקה */
window.deleteUser = function (username) {
  if (!confirm(`למחוק את המשתמש “${username}”?`)) return;
  const fd = new FormData();
  fd.append('action', 'delete');
  fd.append('username', username);

  fetch('/user_managment', { method: 'POST', body: fd })
    .then(r => {
      if (r.ok) {
        showToast("✅ המשתמש נמחק");
        loadDynamicContent('/load_user_management');
      } else alert("❌ שגיאה במחיקה");
    });
};

/* במקרה שה-HTML הוצג כחלק מדף מלא ולא דרך loadDynamicContent */
document.addEventListener('DOMContentLoaded', () => initUserForm());
