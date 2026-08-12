// ============================================================
// CodeWithZaid.online — shared behaviour
// Theme switcher (persisted), mobile nav, contact form handling
// ============================================================

(function () {
  "use strict";

  // ---------- Theme ----------
  var root = document.documentElement;
  var STORAGE_KEY = "cwz-theme";

  function applyTheme(theme) {
    if (theme === "light") {
      root.setAttribute("data-theme", "light");
    } else {
      root.removeAttribute("data-theme");
    }
    var toggles = document.querySelectorAll("[data-theme-toggle]");
    toggles.forEach(function (btn) {
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
    });
  }

  function initTheme() {
    var saved = null;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      /* localStorage unavailable */
    }
    applyTheme(saved === "light" ? "light" : "dark");
  }

  function toggleTheme() {
    var current = root.getAttribute("data-theme") === "light" ? "light" : "dark";
    var next = current === "light" ? "dark" : "light";
    applyTheme(next);
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch (e) {
      /* ignore */
    }
  }

  initTheme();

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("[data-theme-toggle]").forEach(function (btn) {
      btn.addEventListener("click", toggleTheme);
    });

    // ---------- Mobile menu ----------
    var hamburger = document.querySelector("[data-hamburger]");
    var navLinks = document.querySelector("[data-nav-links]");
    if (hamburger && navLinks) {
      hamburger.addEventListener("click", function () {
        var isOpen = navLinks.classList.toggle("open");
        hamburger.classList.toggle("open", isOpen);
        hamburger.setAttribute("aria-expanded", isOpen ? "true" : "false");
      });
      navLinks.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
          navLinks.classList.remove("open");
          hamburger.classList.remove("open");
          hamburger.setAttribute("aria-expanded", "false");
        });
      });
    }

    // ---------- Contact form (front-end demo handling) ----------
    var form = document.querySelector("[data-contact-form]");
    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        var successMsg = document.querySelector("[data-form-success]");
        if (successMsg) {
          successMsg.style.display = "block";
        }
        form.reset();
      });
    }
  });
})();
