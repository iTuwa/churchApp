// Simple text-to-speech helper using the Web Speech API
function speakText(elementId) {
    const el = document.getElementById(elementId);
    if (!el || !window.speechSynthesis) {
        alert('Text-to-speech is not supported in this browser.');
        return;
    }
    const text = el.innerText || el.textContent;
    if (!text) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1.0;
    window.speechSynthesis.speak(utterance);
}

// Local storage for prayer notes
(function () {
    const textarea = document.getElementById('prayer-notes');
    const status = document.getElementById('prayer-notes-status');
    if (!textarea) return;

    const STORAGE_KEY = 'church_app_prayer_notes_v1';

    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
            textarea.value = saved;
        }
    } catch (e) {
        // localStorage might be unavailable; fail silently
    }

    let timeoutId = null;

    textarea.addEventListener('input', function () {
        if (timeoutId) window.clearTimeout(timeoutId);
        status && (status.textContent = 'Saving...');
        timeoutId = window.setTimeout(function () {
            try {
                localStorage.setItem(STORAGE_KEY, textarea.value || '');
                status && (status.textContent = 'Saved locally.');
            } catch (e) {
                status && (status.textContent = 'Could not save locally.');
            }
        }, 400);
    });
})();

// Splash screen hide logic (home page only)
window.addEventListener('load', function () {
    var splash = document.getElementById('splash-screen');
    if (!splash) return;
    // small delay for effect
    setTimeout(function () {
        splash.classList.add('opacity-0', 'pointer-events-none');
        // fully remove after transition
        setTimeout(function () {
            if (splash && splash.parentNode) {
                splash.parentNode.removeChild(splash);
            }
        }, 800);
    }, 800);
});

// Page navigation loading overlay
(function () {
    var loader = document.getElementById('page-loading');
    if (!loader) return;

    function showLoader() {
        loader.classList.remove('opacity-0', 'pointer-events-none');
    }

    // Show loader on link clicks and form submits
    window.addEventListener('DOMContentLoaded', function () {
        var links = document.querySelectorAll('a[href]');
        links.forEach(function (a) {
            var href = a.getAttribute('href');
            if (!href || href.charAt(0) === '#' || a.target === '_blank') return;
            a.addEventListener('click', function (e) {
                // Ignore modifier keys (open in new tab, etc.)
                if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
                showLoader();
            });
        });

        var forms = document.querySelectorAll('form');
        forms.forEach(function (f) {
            f.addEventListener('submit', function () {
                showLoader();
            });
        });
    });
})();

// Simple in-app notifications for new content on home screen
(function () {
    var root = document.getElementById('home-root');
    if (!root) return;

    function maybeNotify(key, label) {
        var latest = root.getAttribute('data-latest-' + key);
        if (!latest) return null;
        var storageKey = 'church_app_last_seen_' + key;
        var lastSeen = null;
        try {
            lastSeen = localStorage.getItem(storageKey);
        } catch (e) {}

        if (!lastSeen || lastSeen < latest) {
            try {
                localStorage.setItem(storageKey, latest);
            } catch (e) {}
            return label;
        }
        return null;
    }

    var messages = [];
    var devoMsg = maybeNotify('devotional', 'A new devotional guide is available.');
    if (devoMsg) messages.push(devoMsg);
    var eventMsg = maybeNotify('event', 'A new church event has been posted.');
    if (eventMsg) messages.push(eventMsg);
    var annMsg = maybeNotify('announcement', 'There is a new announcement.');
    if (annMsg) messages.push(annMsg);

    if (!messages.length) return;

    var bar = document.createElement('div');
    bar.className = 'fixed top-3 inset-x-0 flex justify-center z-30';
    var inner = document.createElement('div');
    inner.className = 'max-w-md mx-auto px-3';
    var box = document.createElement('div');
    box.className = 'rounded-2xl bg-indigo-600 text-white text-xs px-3 py-2 shadow-lg flex items-start gap-2';
    box.innerHTML = '<span>🔔</span><div>' + messages.map(function (m) { return '<p>' + m + '</p>'; }).join('') + '</div>';
    inner.appendChild(box);
    bar.appendChild(inner);
    document.body.appendChild(bar);

    setTimeout(function () {
        box.classList.add('opacity-0');
        setTimeout(function () {
            if (bar && bar.parentNode) {
                bar.parentNode.removeChild(bar);
            }
        }, 600);
    }, 5000);
})();
