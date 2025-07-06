document.addEventListener('DOMContentLoaded', function () {
    const installmentChoiceField = document.querySelector('#installment_choice');
    const installmentCountField = document.querySelector('#installment_count');

    installmentCountField.parentNode.parentNode.style.display = 'none';
    installmentCountField.required = false;

    installmentChoiceField.addEventListener('change', function (e) {
        if (installmentChoiceField.value === '0') {
            installmentCountField.parentNode.parentNode.style.display = 'flex';
            installmentCountField.required = true;
        } else {
            installmentCountField.parentNode.parentNode.style.display = 'none';
            installmentCountField.required = false;
        }
    });

    function checkFormValidation() {
        return !(installmentChoiceField.value === '0' && installmentCountField.value === '');
    }
});