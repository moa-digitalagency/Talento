/**
 * Script de logging des erreurs JavaScript côté client
 * Envoie les erreurs au serveur pour analyse et débogage
 */

(function() {
    'use strict';
    
    // Configuration
    const ERROR_LOG_ENDPOINT = '/api/v1/log-client-error';
    const MAX_ERRORS_PER_SESSION = 50; // Limiter le nombre d'erreurs envoyées
    let errorCount = 0;
    
    // Fonction pour envoyer l'erreur au serveur
    function sendErrorToServer(errorData) {
        if (errorCount >= MAX_ERRORS_PER_SESSION) {
            console.warn('Limite d\'envoi d\'erreurs atteinte pour cette session');
            return;
        }
        
        errorCount++;
        
        // Envoyer l'erreur de manière asynchrone sans bloquer l'application
        if (navigator.sendBeacon) {
            // Utiliser sendBeacon avec un Blob pour spécifier le type application/json
            const blob = new Blob(
                [JSON.stringify(errorData)], 
                { type: 'application/json' }
            );
            navigator.sendBeacon(ERROR_LOG_ENDPOINT, blob);
        } else {
            // Fallback avec fetch
            fetch(ERROR_LOG_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(errorData),
                keepalive: true
            }).catch(function(err) {
                // Silencieux si l'envoi échoue pour ne pas créer de boucle d'erreurs
                console.warn('Impossible d\'envoyer l\'erreur au serveur:', err);
            });
        }
    }
    
    // Capturer les erreurs JavaScript non gérées
    window.addEventListener('error', function(event) {
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
        
        console.error('❌ Erreur JavaScript détectée:', errorData);
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
        
        console.error('❌ Promise rejetée non gérée:', errorData);
        sendErrorToServer(errorData);
    });
    
    // Capturer les erreurs de ressources (images, scripts, etc.)
    window.addEventListener('error', function(event) {
        if (event.target !== window && event.target.tagName) {
            const errorData = {
                type: 'resource_error',
                message: 'Failed to load resource',
                resourceType: event.target.tagName,
                resourceSrc: event.target.src || event.target.href || 'unknown',
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            };
            
            console.warn('⚠️ Erreur de chargement de ressource:', errorData);
            sendErrorToServer(errorData);
        }
    }, true);
    
    // Log console.error pour capture additionnelle
    const originalConsoleError = console.error;
    console.error = function() {
        // Appeler le console.error original
        originalConsoleError.apply(console, arguments);
        
        // Envoyer au serveur
        try {
            const args = Array.from(arguments);
            const errorData = {
                type: 'console_error',
                message: args.map(arg => 
                    typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
                ).join(' '),
                url: window.location.href,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            };
            
            sendErrorToServer(errorData);
        } catch (err) {
            // Ignorer les erreurs dans le logger lui-même
        }
    };
    
    // Logger les informations de session au démarrage
    console.log('📊 Error Logger initialisé');
    console.log('Browser:', navigator.userAgent);
    console.log('URL:', window.location.href);
    
})();
