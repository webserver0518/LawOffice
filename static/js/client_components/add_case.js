/* static/js/client_components/add_case.js */


window.init_add_case = function() {
  initFileUploader();
  initAccordionSections();
  initCaseFormPreview();
  initClientAutocomplete();
  initCategoryAutocomplete();
};

/* עוטפים במיידי – לא מחכים ל-DOMContentLoaded */
(() => {

  /* נחשף ל־window כדי ש-base_dashboard.js יוכל לקרוא */
  window.initFileUploader = function () {

    /* לא לרוץ אם הדף הנוכחי לא מכיל drop-area */
    const dropArea  = document.getElementById('drop-area');
    if (!dropArea || window.__fileUploaderReady) return;

    window.__fileUploaderReady = true;   // דגל שנאתחל פעם אחת
    const pickInput = document.getElementById('fileElem');
    const tbody     = document.querySelector('#fileTable tbody');
    const form      = document.getElementById('upload-form');

    /* יצירת הקלט האמתי */
    let realInput = document.getElementById('realFileInput');
    if (!realInput) {
      realInput          = document.createElement('input');
      realInput.type     = 'file';
      realInput.name     = 'files';
      realInput.id       = 'realFileInput';
      realInput.hidden   = true;
      realInput.multiple = true;
      form.appendChild(realInput);
    }

    const dt        = new DataTransfer();
    const nameCount = {};

    //const stop = e => { e.preventDefault(); e.stopPropagation(); };
    
    ['dragenter','dragover','dragleave','drop'].forEach(ev =>
      window.addEventListener(ev, stop, false));

    dropArea.addEventListener('dragover', () => dropArea.classList.add('highlight'));
    dropArea.addEventListener('dragleave',() => dropArea.classList.remove('highlight'));

    dropArea.addEventListener('drop', e => {
      dropArea.classList.remove('highlight');
      if (e.dataTransfer.files.length) addFiles(e.dataTransfer.files);
    });

    pickInput.addEventListener('change', () => addFiles(pickInput.files));

    /*  הוספת קבצים  */
    function addFiles(list){
      [...list].forEach(f => { dt.items.add(f); addRow(f); });
      realInput.files = dt.files;
      pickInput.value = '';
    }

    function unique(name){
      if (nameCount[name] === undefined) { nameCount[name] = 0; return name; }
      nameCount[name] += 1;
      const dot = name.lastIndexOf('.');
      return dot>-1
        ? `${name.slice(0,dot)}_${nameCount[name]}${name.slice(dot)}`
        : `${name}_${nameCount[name]}`;
    }

    function addRow(file){
      const disp = unique(file.name);
      const tr   = document.createElement('tr');
      tr.innerHTML = `
        <td>${disp}</td>
        <td>
          <select class="form-select form-select-sm" name="file_type_${disp}">
            <option value="general">מסמך כללי</option>
            <option value="appendix">נספח</option>
            <option value="invoice">חשבונית</option>
          </select>
        </td>
        <td class="text-center">
          <button type="button" class="btn btn-sm btn-outline-danger">✖</button>
        </td>`;
      tr.querySelector('button').onclick = () => {
        const idx = [...tbody.children].indexOf(tr);
        dt.items.remove(idx);
        tr.remove();
        realInput.files = dt.files;
      };
      tbody.appendChild(tr);
    }
  };

})();



window.initAccordionSections = function () {
  const headers = document.querySelectorAll(".section-header");

  headers.forEach(header => {
    const targetId = header.getAttribute("data-target");
    const content = document.querySelector(targetId);
    if (!content) return;

    content.style.height = "0";
    content.style.overflow = "hidden";
    content.style.transition = "height 0.5s ease";
    content.classList.remove("show");

    header.addEventListener("click", () => {
      const isOpen = content.classList.contains("show");

      // ⛔ קודם נסגור את כל שאר הסקשנים
      document.querySelectorAll(".accordion-collapse.show").forEach(openItem => {
        if (openItem !== content) {
          openItem.style.height = `${openItem.scrollHeight}px`;
          requestAnimationFrame(() => {
            openItem.style.height = "0";
          });
          openItem.classList.remove("show");
          openItem.previousElementSibling?.querySelector(".section-header")?.classList.add("collapsed");
        }
      });

      // ✅ ואז נטפל בסקשן הנוכחי
      if (isOpen) {
        content.style.height = `${content.scrollHeight}px`;
        requestAnimationFrame(() => {
          content.style.height = "0";
        });
        content.classList.remove("show");
        header.classList.add("collapsed");
      } else {
        content.classList.add("show");
        content.style.height = "0";
        requestAnimationFrame(() => {
          content.style.height = `${content.scrollHeight}px`;
        });
        content.addEventListener("transitionend", () => {
          if (content.classList.contains("show")) {
            content.style.height = "auto";
          }
        }, { once: true });
        header.classList.remove("collapsed");
      }
    });
  });
};




window.initCaseFormPreview = function () {
  const form = document.getElementById("new-case-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    const files = formData.getAll("files");
    const maxSize = 10 * 1024 * 1024; // 10MB

    if (files && Array.isArray(files)) {
      for (const f of files) {
        if (f.size > maxSize) {
          showToast(`❌ הקובץ "${f.name}" חורג מהמגבלה`, true);
          return;
        }
      }
    }

    try {
      const response = await fetch("/client_create", {
        method: "POST",
        body: formData
      });

      if (response.ok) {
        showToast("התיק נוסף בהצלחה");

        // 🔁 שמור בתפריט תתי־דפים
        localStorage.setItem("selectedSubMenu", "all_cases");
        localStorage.setItem("activeSubMenuText", "תיקים פעילים");

        // 🔁 סימון גם בתפריט העליון (ראשי)
        localStorage.setItem("activeMainMenuText", "כל התיקים");

        // 🟩 טען תפריט משנה מחדש
        await showSubMenu("all_cases");

        // ⬇️ טען את תיקים פעילים
        loadDynamicContent("/load_active_cases");

        // ✨ הדגש את תת-הכפתור של תיקים פעילים
        const subLinks = document.querySelectorAll('.sub-sidebar a');
        subLinks.forEach(link => {
          if (link.textContent.trim() === "תיקים פעילים") {
            highlightSubMenu(link);
          }
        });

        // ✨ הדגש גם את הכפתור הראשי
        const mainLinks = document.querySelectorAll('.sidebar a');
        mainLinks.forEach(link => {
          if (link.textContent.trim() === "כל התיקים") {
            highlightMainMenu(link);
          }
        });

      } else {
        showToast("❌ שליחת הטופס נכשלה", true);
      }

    } catch (err) {
      console.error("שגיאה:", err);
      showToast("⚠️ שגיאה כללית בשליחת הטופס", true);
    }
  });
};








window.initClientAutocomplete = async function () {
  const input = document.getElementById("client-name-input");
  const suggestions = document.getElementById("client-suggestions");

  if (!input || !suggestions) return;

  let clients = [];

  try {
    const res = await fetch("/static/data/clients.json");
    clients = await res.json();
    console.log("לקוחות נטענו:", clients);
  } catch (err) {
    console.error("שגיאה בטעינת קובץ לקוחות:", err);
    return;
  }

  function showSuggestions(filter = "") {
    suggestions.innerHTML = "";

    if (!filter) return;

    const matches = clients
      .map(client => ({
        ...client,
        score: client.name.startsWith(filter) ? 0 :
               client.name.toLowerCase().includes(filter.toLowerCase()) ? 1 : 2
      }))
      .filter(c => c.score < 2)
      .sort((a, b) => a.score - b.score)
      .slice(0, 10); // מקסימום 10 הצעות

    matches.forEach(client => {
      const li = document.createElement("li");
      li.className = "list-group-item list-group-item-action";
      li.textContent = client.name;

      li.addEventListener("click", () => {
        input.value = client.name;
        suggestions.innerHTML = "";
        fillClientFields(client);
      });

      suggestions.appendChild(li);
    });
  }

  input.addEventListener("input", () => {
    const value = input.value.trim();
    showSuggestions(value);

    const exactMatch = clients.find(c => c.name === value);
    if (!exactMatch) {
      clearClientFields(true);
    }
  });

  input.addEventListener("focus", () => {
    showSuggestions(input.value.trim());
  });

  input.addEventListener("blur", () => {
    const value = input.value.trim();
    const exactMatch = clients.find(c => c.name === value);
    if (exactMatch) {
      fillClientFields(exactMatch);
    } else {
      clearClientFields(true);
    }
  });

  document.addEventListener("click", (e) => {
    if (!suggestions.contains(e.target) && e.target !== input) {
      suggestions.innerHTML = "";
    }
  });

  function fillClientFields(client) {
    const phone = document.querySelector('[name="client_phone"]');
    const email = document.querySelector('[name="client_email"]');
    const address = document.querySelector('[name="client_address"]');

    phone.value = client.phone || "";
    email.value = client.email || "";
    address.value = client.address || "";

    phone.readOnly = true;
    email.readOnly = true;
    address.readOnly = true;

    phone.classList.add("readonly-locked");
    email.classList.add("readonly-locked");
    address.classList.add("readonly-locked");
  }

  function clearClientFields(forceClear = false) {
    const phone = document.querySelector('[name="client_phone"]');
    const email = document.querySelector('[name="client_email"]');
    const address = document.querySelector('[name="client_address"]');

    if (forceClear) {
      phone.value = "";
      email.value = "";
      address.value = "";
    }

    phone.readOnly = false;
    email.readOnly = false;
    address.readOnly = false;

    phone.classList.remove("readonly-locked");
    email.classList.remove("readonly-locked");
    address.classList.remove("readonly-locked");
  }
};


window.initCategoryAutocomplete = function () {
  const input = document.getElementById("category-input");
  const suggestions = document.getElementById("category-suggestions");

  const categories = [
    "אזרחי",
    "אנרגיה",
    "ביטוח",
    "ביטוח לאומי",
    "ביטוח ונזיקין",
    "בנייה",
    "בנקאות",
    "בנקאות ופיננסים",
    "דיני עבודה",
    "דיני משפחה",
    "דיני סביבה",
    "דיני תעבורה",
    "הוצאה לפועל",
    "הגנת הפרטיות",
    "חוזים",
    "חקיקה",
    "חוקות",
    "זכויות אדם",
    "לשון הרע",
    "מקרקעין",
    "משפט אזרחי",
    "משפט בינלאומי",
    "משפט חוקתי",
    "משפט מנהלי",
    "משפט פלילי",
    "משפט פרוצדורלי",
    "משפט רפואי",
    "משפט עסקי",
    "משפט מקוון",
    "נזיקין",
    "נדלן וחוזים",
    "סייבר",
    "עשיית עושר ולא במשפט",
    "פטנטים",
    "פלילי",
    "פרטיות וסייבר",
    "קוד פתוח",
    "קניין רוחני",
    "ראיות אלקטרוניות",
    "רגולציה וממשל",
    "רפואה ומשפט",
    "שמות מתחם",
    "תקשורת",
    "תיירות",
    "תעבורה",
    "שונות"
  ];
  

  function showSuggestions(filter = "") {
    const value = filter.trim();
    suggestions.innerHTML = "";

    const matches = categories.filter(cat =>
      cat.includes(value)
    ).slice(0, 50); // מקסימום שנציג

    matches.forEach(cat => {
      const li = document.createElement("li");
      li.className = "list-group-item list-group-item-action";
      li.textContent = cat;
      li.addEventListener("click", () => {
        input.value = cat;
        suggestions.innerHTML = "";
      });
      suggestions.appendChild(li);
    });
  }

  input.addEventListener("input", () => {
    showSuggestions(input.value);
  });

  // ✨ כשיש פוקוס (קליק) נציג את הכל
  input.addEventListener("focus", () => {
    showSuggestions("");
  });

  // סגירה כשנלחץ בחוץ
  document.addEventListener("click", (e) => {
    if (!suggestions.contains(e.target) && e.target !== input) {
      suggestions.innerHTML = "";
    }
  });
};

