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
const clearBtn = document.getElementById('clearBtn');
const DEFAULT_MARKDOWN = `# Styled Markdown Example

This is a paragraph with **bold** and *italic* text.

## Lists Example
- First item
- Second item with **bold**
- Nested item with *italic*
- Another nested item
- Third item

## Java Code Example
\`\`\`javascript
function greeting(name) {
  return \`Hello, \${name}!\`;
}
\`\`\`

## Python Example
\`\`\`python
def fibonacci(n):
    if n <= 1:
        return n
    else:
        a, b = 0, 1
        for _ in range(n - 1):
            a, b = b, a + b
        return b

# List comprehension example
squares = [x**2 for x in range(10)]
\`\`\`

## Blockquote Example
> This is a blockquote.
> It can span multiple lines.

## Table Example
| Feature | Description |
|---------|-------------|
| Tables  | Organized data display |
| Lists   | Bullet points and numbers |
| Code    | Syntax highlighted blocks |

## Link Example
[Visit GitHub](https://github.com)

***

### Cat Image Example
![Placeholder Image](https://images.unsplash.com/photo-1533743983669-94fa5c4338ec?q=80&w=800&auto=format&fit=crop)
`;





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
editor.addEventListener('input', function () {
    updatePreview();
    saveCurrentDocument();
});

docNameInput.addEventListener('input', function () {
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

clearBtn.addEventListener('click', () => {
    editor.value = '';
    updatePreview()
});

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
        item.addEventListener('click', function () {
            loadDocument(this.getAttribute('data-doc-id'));
        });
    });
}

newDocBtn.addEventListener('click', function () {
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
downloadBtn.addEventListener('click', async function () {
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

        // Get the base64 string from response
        const pdfBase64 = await response.text();

        // Convert base64 to binary
        const binaryString = atob(pdfBase64);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        // Create blob from binary data
        const blob = new Blob([bytes], { type: 'application/pdf' });
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
        showError(error.message || 'Failed to generate PDF');
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
editor.value = DEFAULT_MARKDOWN;
updatePreview();
renderDocumentList();
