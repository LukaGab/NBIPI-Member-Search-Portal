document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const searchForm = document.getElementById('searchForm');
    const lastNameInput = document.getElementById('last_name');
    const memberNumberInput = document.getElementById('member_number');

    searchForm.addEventListener('submit', function(event) {
        const lastName = lastNameInput.value.trim();
        const memberNumber = memberNumberInput.value.trim();

        if (!lastName && !memberNumber) {
            event.preventDefault();
            alert('Please enter either a last name or member number');
            return false;
        }

        // Validate member number format if provided
        if (memberNumber && !memberNumber.match(/^M\d{3}$/i)) {
            event.preventDefault();
            alert('Member number should be in the format M001');
            return false;
        }
    });

    // Clear form handler
    const resetButton = searchForm.querySelector('button[type="reset"]');
    resetButton.addEventListener('click', function() {
        // Remove any existing alerts
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => alert.remove());
    });
});
