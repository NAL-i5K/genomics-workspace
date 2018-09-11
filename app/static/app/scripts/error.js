window.jsErrors = [];
window.onerror = function(errorMessage) {
    window.jsErrors[window.jsErrors.length] = errorMessage;
}
