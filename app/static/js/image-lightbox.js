class ImageLightbox {
    constructor() {
        this.currentIndex = 0;
        this.images = [];
        this.lightbox = null;
        this.init();
    }

    init() {
        this.createLightboxHTML();
        this.attachEventListeners();
    }

    createLightboxHTML() {
        const lightboxHTML = `
            <div id="image-lightbox" class="lightbox-overlay">
                <div class="lightbox-container">
                    <button class="lightbox-close" aria-label="Fermer">&times;</button>
                    <button class="lightbox-prev" aria-label="Précédent">&#10094;</button>
                    <button class="lightbox-next" aria-label="Suivant">&#10095;</button>
                    <img class="lightbox-image" src="" alt="">
                    <div class="lightbox-counter"></div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', lightboxHTML);
        this.lightbox = document.getElementById('image-lightbox');
    }

    attachEventListeners() {
        const closeBtn = this.lightbox.querySelector('.lightbox-close');
        const prevBtn = this.lightbox.querySelector('.lightbox-prev');
        const nextBtn = this.lightbox.querySelector('.lightbox-next');

        closeBtn.addEventListener('click', () => this.close());
        prevBtn.addEventListener('click', () => this.prev());
        nextBtn.addEventListener('click', () => this.next());

        this.lightbox.addEventListener('click', (e) => {
            if (e.target === this.lightbox) {
                this.close();
            }
        });

        document.addEventListener('keydown', (e) => {
            if (!this.lightbox.classList.contains('active')) return;
            
            if (e.key === 'Escape') this.close();
            if (e.key === 'ArrowLeft') this.prev();
            if (e.key === 'ArrowRight') this.next();
        });
    }

    open(imageSrc, imagesList = null) {
        if (imagesList && imagesList.length > 0) {
            this.images = imagesList;
            this.currentIndex = this.images.indexOf(imageSrc);
            if (this.currentIndex === -1) {
                this.images.unshift(imageSrc);
                this.currentIndex = 0;
            }
        } else {
            this.images = [imageSrc];
            this.currentIndex = 0;
        }

        this.updateImage();
        this.lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
        
        this.updateNavigation();
    }

    close() {
        this.lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }

    prev() {
        if (this.images.length <= 1) return;
        this.currentIndex = (this.currentIndex - 1 + this.images.length) % this.images.length;
        this.updateImage();
        this.updateNavigation();
    }

    next() {
        if (this.images.length <= 1) return;
        this.currentIndex = (this.currentIndex + 1) % this.images.length;
        this.updateImage();
        this.updateNavigation();
    }

    updateImage() {
        const img = this.lightbox.querySelector('.lightbox-image');
        img.src = this.images[this.currentIndex];
        
        const counter = this.lightbox.querySelector('.lightbox-counter');
        if (this.images.length > 1) {
            counter.textContent = `${this.currentIndex + 1} / ${this.images.length}`;
            counter.style.display = 'block';
        } else {
            counter.style.display = 'none';
        }
    }

    updateNavigation() {
        const prevBtn = this.lightbox.querySelector('.lightbox-prev');
        const nextBtn = this.lightbox.querySelector('.lightbox-next');

        if (this.images.length <= 1) {
            prevBtn.style.display = 'none';
            nextBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'flex';
            nextBtn.style.display = 'flex';
        }
    }
}

let lightboxInstance = null;

document.addEventListener('DOMContentLoaded', function() {
    lightboxInstance = new ImageLightbox();

    document.querySelectorAll('.lightbox-trigger').forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            const imageSrc = this.getAttribute('data-image-src') || this.src;
            const galleryGroup = this.getAttribute('data-gallery');
            
            let galleryImages = null;
            if (galleryGroup) {
                galleryImages = Array.from(
                    document.querySelectorAll(`.lightbox-trigger[data-gallery="${galleryGroup}"]`)
                ).map(img => img.getAttribute('data-image-src') || img.src);
            }
            
            lightboxInstance.open(imageSrc, galleryImages);
        });
    });
});
