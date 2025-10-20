class BulkActionManager {
    constructor() {
        this.selectedIds = new Set();
        this.toolbar = null;
        this.selectAllCheckbox = null;
        this.init();
    }

    init() {
        this.createToolbar();
        this.attachEventListeners();
    }

    createToolbar() {
        const toolbar = document.createElement('div');
        toolbar.id = 'bulk-action-toolbar';
        toolbar.className = 'fixed bottom-8 left-1/2 transform -translate-x-1/2 bg-white shadow-2xl rounded-lg border-2 border-blue-500 p-4 hidden z-50';
        toolbar.innerHTML = `
            <div class="flex items-center gap-4">
                <span class="text-sm font-semibold text-gray-700">
                    <span id="selected-count">0</span> sélectionné(s)
                </span>
                <div class="flex gap-2">
                    <button onclick="bulkManager.exportSelected('pdf')" 
                            class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-all flex items-center gap-2 text-sm font-semibold">
                        <span>📄</span>
                        <span>PDF</span>
                    </button>
                    <button onclick="bulkManager.exportSelected('csv')" 
                            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-all flex items-center gap-2 text-sm font-semibold">
                        <span>📊</span>
                        <span>CSV</span>
                    </button>
                    <button onclick="bulkManager.exportSelected('excel')" 
                            class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-all flex items-center gap-2 text-sm font-semibold">
                        <span>📗</span>
                        <span>Excel</span>
                    </button>
                    <button onclick="bulkManager.deleteSelected()" 
                            class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 transition-all flex items-center gap-2 text-sm font-semibold">
                        <span>🗑️</span>
                        <span>Supprimer</span>
                    </button>
                    <button onclick="bulkManager.clearSelection()" 
                            class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-all text-sm font-semibold">
                        ✕
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(toolbar);
        this.toolbar = toolbar;
    }

    attachEventListeners() {
        document.addEventListener('change', (e) => {
            if (e.target.classList.contains('user-checkbox')) {
                this.handleCheckboxChange(e.target);
            } else if (e.target.id === 'select-all-checkbox') {
                this.handleSelectAll(e.target);
            }
        });
    }

    handleCheckboxChange(checkbox) {
        const userId = parseInt(checkbox.value);
        if (checkbox.checked) {
            this.selectedIds.add(userId);
        } else {
            this.selectedIds.delete(userId);
        }
        this.updateToolbar();
        this.updateSelectAllState();
    }

    handleSelectAll(checkbox) {
        const userCheckboxes = document.querySelectorAll('.user-checkbox');
        userCheckboxes.forEach(cb => {
            cb.checked = checkbox.checked;
            const userId = parseInt(cb.value);
            if (checkbox.checked) {
                this.selectedIds.add(userId);
            } else {
                this.selectedIds.delete(userId);
            }
        });
        this.updateToolbar();
    }

    updateSelectAllState() {
        const selectAllCheckbox = document.getElementById('select-all-checkbox');
        if (!selectAllCheckbox) return;

        const userCheckboxes = document.querySelectorAll('.user-checkbox');
        const checkedCheckboxes = document.querySelectorAll('.user-checkbox:checked');
        
        selectAllCheckbox.checked = userCheckboxes.length > 0 && userCheckboxes.length === checkedCheckboxes.length;
        selectAllCheckbox.indeterminate = checkedCheckboxes.length > 0 && checkedCheckboxes.length < userCheckboxes.length;
    }

    updateToolbar() {
        const count = this.selectedIds.size;
        document.getElementById('selected-count').textContent = count;
        
        if (count > 0) {
            this.toolbar.classList.remove('hidden');
        } else {
            this.toolbar.classList.add('hidden');
        }
    }

    clearSelection() {
        this.selectedIds.clear();
        document.querySelectorAll('.user-checkbox').forEach(cb => cb.checked = false);
        const selectAllCheckbox = document.getElementById('select-all-checkbox');
        if (selectAllCheckbox) selectAllCheckbox.checked = false;
        this.updateToolbar();
    }

    exportSelected(format) {
        if (this.selectedIds.size === 0) {
            alert('Veuillez sélectionner au moins un utilisateur');
            return;
        }

        const ids = Array.from(this.selectedIds).join(',');
        const url = `/admin/bulk/export?format=${format}&ids=${ids}`;
        window.location.href = url;
    }

    deleteSelected() {
        if (this.selectedIds.size === 0) {
            alert('Veuillez sélectionner au moins un utilisateur');
            return;
        }

        const count = this.selectedIds.size;
        if (!confirm(`⚠️ Êtes-vous sûr de vouloir supprimer ${count} utilisateur(s) ? Cette action est irréversible.`)) {
            return;
        }

        const ids = Array.from(this.selectedIds);
        
        fetch('/admin/bulk/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ ids: ids })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`✅ ${data.deleted_count} utilisateur(s) supprimé(s) avec succès`);
                location.reload();
            } else {
                alert(`❌ Erreur: ${data.error}`);
            }
        })
        .catch(error => {
            alert('Erreur lors de la suppression: ' + error);
        });
    }
}

let bulkManager;
document.addEventListener('DOMContentLoaded', () => {
    bulkManager = new BulkActionManager();
});
