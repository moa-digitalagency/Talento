class ImageCropperManager {
    constructor() {
        this.cropper = null;
        this.currentInput = null;
        this.currentFile = null;
        this.modal = null;
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.createModalHTML();
        this.attachEventListeners();
    }

    createModalHTML() {
        const modalHTML = `
            <div id="image-cropper-modal" class="cropper-modal-overlay">
                <div class="cropper-modal-container">
                    <div class="cropper-modal-header">
                        <h3 class="cropper-modal-title">Recadrer votre photo</h3>
                        <button class="cropper-close-btn" aria-label="Fermer">&times;</button>
                    </div>
                    <div class="cropper-modal-body">
                        <div class="cropper-container">
                            <img id="cropper-image" src="" alt="Image à recadrer">
                        </div>
                        <p class="cropper-instructions">
                            💡 <strong>Conseil :</strong> Utilisez la molette de la souris ou les boutons ci-dessous pour zoomer et positionner votre photo.
                        </p>
                    </div>
                    <div class="cropper-modal-actions">
                        <button type="button" class="cropper-btn cropper-btn-zoom-in" title="Zoomer">
                            <span>🔍+</span> Zoom +
                        </button>
                        <button type="button" class="cropper-btn cropper-btn-zoom-out" title="Dézoomer">
                            <span>🔍-</span> Zoom -
                        </button>
                        <button type="button" class="cropper-btn cropper-btn-rotate" title="Rotation">
                            <span>🔄</span> Rotation
                        </button>
                        <button type="button" class="cropper-btn cropper-btn-cancel">
                            <span>❌</span> Annuler
                        </button>
                        <button type="button" class="cropper-btn cropper-btn-confirm cropper-btn-primary">
                            <span>✅</span> Valider
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        this.modal = document.getElementById('image-cropper-modal');
    }

    attachEventListeners() {
        const closeBtn = this.modal.querySelector('.cropper-close-btn');
        const cancelBtn = this.modal.querySelector('.cropper-btn-cancel');
        const confirmBtn = this.modal.querySelector('.cropper-btn-confirm');
        const zoomInBtn = this.modal.querySelector('.cropper-btn-zoom-in');
        const zoomOutBtn = this.modal.querySelector('.cropper-btn-zoom-out');
        const rotateBtn = this.modal.querySelector('.cropper-btn-rotate');

        closeBtn.addEventListener('click', () => this.close());
        cancelBtn.addEventListener('click', () => this.close());
        confirmBtn.addEventListener('click', () => this.confirm());
        zoomInBtn.addEventListener('click', () => this.zoom(0.1));
        zoomOutBtn.addEventListener('click', () => this.zoom(-0.1));
        rotateBtn.addEventListener('click', () => this.rotate());

        this.modal.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.close();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (!this.modal.classList.contains('active')) return;
            if (e.key === 'Escape') this.close();
        });
    }

    initializeCropper(inputElement) {
        const file = inputElement.files[0];
        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Veuillez sélectionner une image valide.');
            inputElement.value = '';
            return;
        }

        const maxSize = 5 * 1024 * 1024;
        if (file.size > maxSize) {
            alert('La photo ne doit pas dépasser 5 MB.');
            inputElement.value = '';
            return;
        }

        this.currentInput = inputElement;
        this.currentFile = file;

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = this.modal.querySelector('#cropper-image');
            img.src = e.target.result;
            this.open();
        };
        reader.readAsDataURL(file);
    }

    open() {
        this.modal.classList.add('active');
        document.body.style.overflow = 'hidden';

        const img = this.modal.querySelector('#cropper-image');
        
        if (this.cropper) {
            this.cropper.destroy();
        }

        this.cropper = new Cropper(img, {
            aspectRatio: 1,
            viewMode: 1,
            dragMode: 'move',
            autoCropArea: 1,
            restore: false,
            guides: true,
            center: true,
            highlight: false,
            cropBoxMovable: true,
            cropBoxResizable: true,
            toggleDragModeOnDblclick: false,
            responsive: true,
            background: true,
            modal: true,
            minContainerWidth: 200,
            minContainerHeight: 200
        });
    }

    close(skipResetInput = false) {
        this.modal.classList.remove('active');
        document.body.style.overflow = '';
        
        if (this.cropper) {
            this.cropper.destroy();
            this.cropper = null;
        }

        if (this.currentInput && !skipResetInput) {
            this.currentInput.value = '';
        }
        
        if (!skipResetInput) {
            this.currentInput = null;
            this.currentFile = null;
        }
    }

    zoom(ratio) {
        if (this.cropper) {
            this.cropper.zoom(ratio);
        }
    }

    rotate() {
        if (this.cropper) {
            this.cropper.rotate(90);
        }
    }

    confirm() {
        if (!this.cropper || !this.currentInput) return;

        this.isProcessing = true;

        this.cropper.getCroppedCanvas({
            width: 800,
            height: 800,
            imageSmoothingEnabled: true,
            imageSmoothingQuality: 'high',
        }).toBlob((blob) => {
            const fileName = this.currentFile.name;
            const croppedFile = new File([blob], fileName, {
                type: 'image/jpeg',
                lastModified: Date.now()
            });

            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(croppedFile);
            this.currentInput.files = dataTransfer.files;

            this.showPreview(this.currentInput);
            
            this.close(true);
            
            this.currentInput = null;
            this.currentFile = null;
            this.isProcessing = false;
        }, 'image/jpeg', 0.95);
    }

    showPreview(inputElement) {
        const previewId = inputElement.id + '-preview';
        const existingPreview = document.getElementById(previewId);
        
        if (existingPreview) {
            existingPreview.remove();
        }

        const file = inputElement.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const previewHTML = `
                    <div id="${previewId}" class="mt-4 text-center">
                        <p class="text-sm text-gray-600 mb-2">✅ Photo recadrée avec succès</p>
                        <img src="${e.target.result}" alt="Aperçu" class="mx-auto w-32 h-32 object-cover rounded-lg border-2 border-green-500 shadow-lg">
                    </div>
                `;
                inputElement.parentElement.insertAdjacentHTML('beforeend', previewHTML);
            };
            reader.readAsDataURL(file);
        }
    }
}

let cropperManager = null;

document.addEventListener('DOMContentLoaded', function() {
    cropperManager = new ImageCropperManager();

    const photoInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    photoInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            if (cropperManager.isProcessing) {
                return;
            }
            
            if (this.files && this.files.length > 0) {
                if (this.multiple) {
                    return;
                }
                
                e.preventDefault();
                e.stopPropagation();
                
                cropperManager.initializeCropper(this);
            }
        });
    });
});
