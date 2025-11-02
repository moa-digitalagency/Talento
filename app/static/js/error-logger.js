/**
 * Script de logging des erreurs JavaScript côté client
 * Envoie les erreurs critiques au serveur pour analyse et débogage
 */

(function() {
    'use strict';
    
    // Configuration
    const ERROR_LOG_ENDPOINT = '/api/v1/log-client-error';
    const MAX_ERRORS_PER_SESSION = 10; // Réduire le nombre d'erreurs envoyées
    let errorCount = 0;
    
    // Liste des erreurs à ignorer (bruit de fond, extensions navigateur, etc.)
    const IGNORED_ERRORS = [
        'beacon.js',
        'chrome-extension://',
        'moz-extension://',
        'safari-extension://',
        'Unknown error', // Erreurs génériques sans contexte
        'Script error', // Erreurs cross-origin
        'ResizeObserver loop', // Erreurs bénignes du navigateur
    ];
    
    // Vérifier si l'erreur doit être ignorée
    function shouldIgnoreError(errorData) {
        // Ignorer si limite atteinte
        if (errorCount >= MAX_ERRORS_PER_SESSION) {
            return true;
        }
        
        // Ignorer les erreurs sans stack trace et sans informations utiles
        if (errorData.message === 'Unknown error' && 
            errorData.filename === 'unknown' && 
            !errorData.stack) {
            return true;
        }
        
        // Ignorer les erreurs de la liste
        const errorString = JSON.stringify(errorData).toLowerCase();
        for (let i = 0; i < IGNORED_ERRORS.length; i++) {
            if (errorString.indexOf(IGNORED_ERRORS[i].toLowerCase()) !== -1) {
                return true;
            }
        }
        
        return false;
    }
    
    // Fonction pour envoyer l'erreur au serveur
    function sendErrorToServer(errorData) {
        if (shouldIgnoreError(errorData)) {
            return;
        }
        
        errorCount++;
        
        // Envoyer l'erreur de manière asynchrone sans bloquer l'application
        try {
            fetch(ERROR_LOG_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(errorData),
                keepalive: true
            }).catch(function() {
                // Silencieux si l'envoi échoue
            });
        } catch (err) {
            // Ignorer les erreurs du logger lui-même
        }
    }
    
    // Capturer les erreurs JavaScript non gérées
    window.addEventListener('error', function(event) {
        // Ignorer les erreurs de ressources (gérées séparément)
        if (event.target !== window) {
            return;
        }
        
        const errorData = {
            type: 'javascript_error',
            message: event.message || 'Unknown error',
            filename: event.filename || 'unknown',
            line: event.lineno || 0,
            column: event.colno || 0,
            stack: event.error && event.error.stack ? event.error.stack : null,
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        
        sendErrorToServer(errorData);
    }, true);
    
    // Capturer les promesses rejetées non gérées
    window.addEventListener('unhandledrejection', function(event) {
        const errorData = {
            type: 'unhandled_promise_rejection',
            message: event.reason ? event.reason.toString() : 'Promise rejection',
            stack: event.reason && event.reason.stack ? event.reason.stack : null,
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        
        sendErrorToServer(errorData);
    });
    
    // Capturer uniquement les erreurs de ressources importantes (scripts et stylesheets)
    window.addEventListener('error', function(event) {
        if (event.target !== window && event.target.tagName) {
            const tagName = event.target.tagName.toLowerCase();
            
            // Ignorer les erreurs d'images (souvent des 404 bénignes)
            if (tagName === 'img') {
                return;
            }
            
            const resourceSrc = event.target.src || event.target.href || 'unknown';
            
            // Ignorer les ressources externes (extensions, CDN tiers non critiques)
            if (resourceSrc.indexOf('chrome-extension://') !== -1 ||
                resourceSrc.indexOf('moz-extension://') !== -1 ||
                resourceSrc.indexOf('beacon.js') !== -1) {
                return;
            }
            
            const errorData = {
                type: 'resource_error',
                message: 'Failed to load resource',
                resourceType: tagName.toUpperCase(),
                resourceSrc: resourceSrc,
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            };
            
            sendErrorToServer(errorData);
        }
    }, true);
    
    // Logger les informations de session au démarrage (une seule fois)
    if (window.console && window.console.log) {
        console.log('📊 Error Logger initialisé - Mode production');
    }
    
})();
