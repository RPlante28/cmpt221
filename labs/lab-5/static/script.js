// navigation
function goNext(nextPage) {
    window.location.href = nextPage;
}

document.addEventListener("DOMContentLoaded", () => {
    const body = document.body;

    if (body.classList.contains("tier2")) fontChaos();
    if (body.classList.contains("tier3")) { fontChaos(); caesarChaos(); }
    if (body.classList.contains("tier4")) { fontChaos(); caesarChaos(); positionChaos(); }
});

// change fonts
const fontList = [
    "Arial", "Courier New", "Times New Roman", "Comic Sans MS",
    "Impact", "Georgia", "Verdana", "Lucida Console", "Tahoma"
];

function fontChaos() {
    wrapChars();
    setInterval(() => {
        document.querySelectorAll("span.char").forEach(span => {
            const randomFont = fontList[Math.floor(Math.random() * fontList.length)];
            span.style.fontFamily = randomFont;
        });
    }, 200);
}

// caesar shifting
let shift = 0;

function caesarChaos() {
    wrapChars();
    setInterval(() => {
        shift = (shift + 1) % 26;
        document.querySelectorAll("span.char").forEach(span => {
            span.textContent = shiftChar(span.textContent, 1);
        });
    }, 1000);
}

function shiftChar(c, s) {
    if (/[a-z]/.test(c)) return String.fromCharCode((c.charCodeAt(0) - 97 + s) % 26 + 97);
    if (/[A-Z]/.test(c)) return String.fromCharCode((c.charCodeAt(0) - 65 + s) % 26 + 65);
    return c;
}

// change position
function positionChaos() {
    wrapChars();
    setInterval(() => {
        document.querySelectorAll("span.char").forEach(span => {
            const angle = Math.random() * 360;
            const distance = Math.random() * 3;
            span.style.transform = `translate(${Math.sin(angle) * distance}px, ${Math.cos(angle) * distance}px)`;
        });
    }, 150);
}

// wrap characters for easier manipulation!
function wrapChars() {
    document.querySelectorAll("body *:not(script):not(style):not(span)").forEach(node => {
        if (node.children.length === 0 && node.textContent.trim().length > 0) {
            node.innerHTML = node.textContent
                .split("")
                .map(c => `<span class="char">${c}</span>`)
                .join("");
        }
    });
}
