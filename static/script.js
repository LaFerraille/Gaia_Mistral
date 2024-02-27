document.getElementById('toggleMenu').addEventListener('click', function () {
    var menu = document.getElementById('leftMenu');
    menu.classList.toggle('hidden');
});

document.getElementById('toggleProfile').addEventListener('click', function () {
    var profile = document.getElementById('rightProfile');
    profile.classList.toggle('hidden');
});