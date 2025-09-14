document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById("themeToggle");
    const html = document.documentElement;
    const themeToggleIcon = document.getElementById("theme-toggle-icon")
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        html.classList.add('dark');
        themeToggleIcon.classList.replace('fa-moon', 'fa-sun');
        document.querySelector('meta[name="theme-color"]').setAttribute('content', '#000000');
    }

    themeToggle.addEventListener('click', (event) => {
        document.documentElement.classList.toggle('dark')
        if (html.classList.contains('dark')) {
            localStorage.setItem('theme', 'dark')
            themeToggleIcon.classList.replace('fa-moon', 'fa-sun');
            document.querySelector('meta[name="theme-color"]').setAttribute('content', '#000000');
        } else {
            localStorage.setItem('theme', 'light')
            themeToggleIcon.classList.replace('fa-sun', 'fa-moon');
            document.querySelector('meta[name="theme-color"]').setAttribute('content', '#0070f3');
        }
    })

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(
        anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();

                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    const headerHeight = document.querySelector('header').offsetHeight;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - headerHeight;
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    })
                }

            })
        }
    )
})


// Set footer current year

const yearElt = document.getElementById('year');

if (yearElt) {
    yearElt.innerHTML = `${(new Date()).getFullYear()}`;
}


function openMapPopup(mapId, visitor_description) {
    console.log("Init map on:", mapId);

    const lat = visitor_description['latitude'];
    const lng = visitor_description['longitude'];

    const container = document.getElementById(mapId);
    if (container._leaflet_id) {
        container._leaflet_id = null; // empêche Leaflet de supprimer le div
    }

    const map = L.map(mapId).setView([lat, lng], 13);
    window[mapId] = map;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    L.marker([lat, lng]).addTo(map)
        .bindPopup('<b>Current position</b>').openPopup();

    const popup = L.popup();
    map.on('click', function (e) {
        popup
            .setLatLng(e.latlng)
            .setContent(`You clicked the map at ${e.latlng.toString()}`)
            .openOn(map);
    });
    setTimeout(() => {
        map.invalidateSize();
    }, 300);
}
