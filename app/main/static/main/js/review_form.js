function updateStars(value) {
    const stars = '★★★★★'.slice(0, value);
    document.getElementById('star-rating').textContent = stars;
}