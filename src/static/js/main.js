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


function open_map() {
	const map = L.map('map').setView([51.505, -0.09], 13);

	const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
		maxZoom: 19,
		attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
	}).addTo(map);

	const marker = L.marker([51.5, -0.09]).addTo(map)
		.bindPopup('<b>Current position</b><br />').openPopup();





	function onMapClick(e) {
		popup
			.setLatLng(e.latlng)
			.setContent(`You clicked the map at ${e.latlng.toString()}`)
			.openOn(map);
	}

	map.on('click', onMapClick);
}