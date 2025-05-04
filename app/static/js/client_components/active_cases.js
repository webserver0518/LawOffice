(() => {
    const tbody = document.querySelector('#activeCasesTable tbody');
    if (!tbody) return;
  
    fetch('/get_active_cases')
      .then(r => r.json())
      .then(rows => {
        if (!Array.isArray(rows) || rows.length === 0) {
          tbody.innerHTML = '<tr><td colspan="4" class="text-center">אין תיקים פעילים</td></tr>';
          return;
        }
        tbody.innerHTML = rows.map(r =>
          `<tr><td>${r.serial}</td>
          <td>${r.case_title}</td></tr>
          <td>${r.client_name}</td></tr>
          <td>${r.category}</td></tr>`
        ).join('');
      })
      .catch(err => {
        console.error(err);
        tbody.innerHTML = '<tr><td colspan="2" class="text-danger text-center">שגיאה בטעינת נתונים</td></tr>';
      });
  })();
  