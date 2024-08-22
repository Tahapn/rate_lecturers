document.addEventListener('DOMContentLoaded', function () {
    var total = 0;
    var ratings = document.querySelectorAll('.progress-bar');
    ratings.forEach(function (bar) {
        total += parseInt(bar.getAttribute('aria-valuenow'));
    });
    ratings.forEach(function (bar) {
        var count = parseInt(bar.getAttribute('aria-valuenow'));
        bar.style.width = (count / total) * 100 + '%';
        bar.textContent = count + ' ratings';
        bar.style.backgroundColor = getColor(bar.getAttribute('data-rating'));
    });

    function getColor(rating) {
        switch (rating) {
            case '5':
                return '#28a745'; // Green
            case '4':
                return '#17a2b8'; // Blue
            case '3':
                return '#ffc107'; // Yellow
            case '2':
                return '#fd7e14'; // Orange
            case '1':
                return '#dc3545'; // Red
            default:
                return '#6c757d'; // Grey
        }
    }
});
