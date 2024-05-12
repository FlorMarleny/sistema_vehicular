document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const inputs = form.querySelectorAll('input, select');

    inputs.forEach(function(input) {
        input.classList.add('form-control');
    });
});
