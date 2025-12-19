const backendUrl = `${globalThis.location.protocol}//${globalThis.location.hostname}`;
const API_URL_CONVERTER = `${backendUrl}/api/convert`;
const md = globalThis.markdownit({
    html: true
});
const loginBtn = document.getElementById('loginBtn')
const editor = document.getElementById('editor');
const preview = document.getElementById('preview');
const downloadBtn = document.getElementById('downloadBtn');
const loading = document.getElementById('loading');
const errorMsg = document.getElementById('errorMsg');
const docName = document.getElementById('docName');
const docNameInput = document.getElementById('docNameInput');
const newDocBtn = document.getElementById('newDocBtn');
const documentList = document.getElementById('documentList');

function getNextUntitledName() {
    const baseName = 'Untitled Document';
    const numbers = documents
        .map(d => {
            const match = d.name.match(/^Untitled Document (\d+)$/);
            return match ? parseInt(match[1], 10) : null;
        })
        .filter(n => n !== null);

    const nextNumber = numbers.length ? Math.max(...numbers) + 1 : 1;
    return `${baseName} ${nextNumber}`;
}

let documents = [
    { id: 'default', name: 'Untitled Document', content: editor.value }
];
let currentDocId = 'default';

// Live preview update
editor.addEventListener('input', function() {
    updatePreview();
    saveCurrentDocument();
});

docNameInput.addEventListener('input', function() {
    const doc = documents.find(d => d.id === currentDocId);
    if (doc) {
        doc.name = docNameInput.value;
        renderDocumentList();
    }
});

function updatePreview() {
    const markdown = editor.value;
    preview.innerHTML = md.render(markdown);
}

function saveCurrentDocument() {
    const doc = documents.find(d => d.id === currentDocId);
    if (doc) {
        doc.content = editor.value;
    }
}

function loadDocument(docId) {
    saveCurrentDocument();
    
    const doc = documents.find(d => d.id === docId);
    if (doc) {
        currentDocId = docId;
        editor.value = doc.content;
        docNameInput.value = doc.name;
        updatePreview();
        
        document.querySelectorAll('.sidebar-item').forEach(item => {
            item.classList.remove('active');
        });
        document.querySelector(`[data-doc-id="${docId}"]`).classList.add('active');
    }
}

function renderDocumentList() {
    documentList.innerHTML = documents.map(doc => `
        <div class="sidebar-item ${doc.id === currentDocId ? 'active' : ''}" data-doc-id="${doc.id}">
            <span class="icon">📄</span>
            <span>${doc.name}</span>
        </div>
    `).join('');

    document.querySelectorAll('.sidebar-item').forEach(item => {
        item.addEventListener('click', function() {
            loadDocument(this.getAttribute('data-doc-id'));
        });
    });
}

newDocBtn.addEventListener('click', function() {
    const newDoc = {
        id: 'doc_' + Date.now(),
        name: getNextUntitledName(),
        content: ''
    };

    documents.push(newDoc);
    renderDocumentList();
    loadDocument(newDoc.id);
});

// Download PDF via API
downloadBtn.addEventListener('click', async function() {
    const markdown = editor.value.trim();
    
    if (!markdown) {
        showError('Please enter some markdown content first!');
        return;
    }

    loading.classList.add('show');
    errorMsg.classList.remove('show');

    try {
        const response = await fetch(API_URL_CONVERTER, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                markdown: markdown,
                filename: docNameInput.value.trim() + '.pdf'
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Failed to generate PDF');
        }

        const blob = await response.blob();
        const url = globalThis.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = docNameInput.value.trim() + '.pdf';
        document.body.appendChild(a);
        a.click();
        globalThis.URL.revokeObjectURL(url);
        document.body.removeChild(a);

    } catch (error) {
        console.error('Error:', error);
        showError(error || 'Failed to generate PDF');
    } finally {
        loading.classList.remove('show');
    }
});


function showError(message) {
    errorMsg.textContent = message;
    errorMsg.classList.add('show');
    setTimeout(() => {
        errorMsg.classList.remove('show');
    }, 5000);
}


document.addEventListener("DOMContentLoaded", () => {
    const editor = document.getElementById("editor");
    const preview = document.getElementById("preview");

    let isSyncingEditorScroll = false;
    let isSyncingPreviewScroll = false;

    function syncScroll(source, target) {
        const sourceScrollTop = source.scrollTop;
        const sourceScrollHeight = source.scrollHeight - source.clientHeight;
        const targetScrollHeight = target.scrollHeight - target.clientHeight;

        if (sourceScrollHeight <= 0 || targetScrollHeight <= 0) return;

        const scrollRatio = sourceScrollTop / sourceScrollHeight;
        target.scrollTop = scrollRatio * targetScrollHeight;
    }

    editor.addEventListener("scroll", () => {
        if (isSyncingEditorScroll) {
            isSyncingEditorScroll = false;
            return;
        }
        isSyncingPreviewScroll = true;
        syncScroll(editor, preview);
    });

    preview.addEventListener("scroll", () => {
        if (isSyncingPreviewScroll) {
            isSyncingPreviewScroll = false;
            return;
        }
        isSyncingEditorScroll = true;
        syncScroll(preview, editor);
    });
});




// Initial preview
updatePreview();
renderDocumentList();
