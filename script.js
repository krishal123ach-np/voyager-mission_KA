let allplanets = [];


fetch('exoplanets.json')
    .then(response => response.json())
    .then(planets => {
        allPlanets = planets;
        document.getElementById('status').textContent = `Loaded ${planets.length} confirmed exoplanets.`;
        renderPlanets(allPlanets);
    })
    .catch(error => {
        document.getElementById('status').textContent = 'Could not load exoplanet data. Check the file path and try again.';
        console.error('Error loading exoplanet data:', error);
    });

    function renderPlanets(planets) {
        const grid = document.getElementById('planetGrid');
        grid.innerHTML = '';
        planets.forEach(planet => {;
            const card = document.createElement('div');
            card.className = 'planet-card';
            const distance = planet.distance_ly !== null ? planet.distance_ly.toFixed(1) + ' light-years' : 'Unknown distance';
            
            card.innerHTML = `
                <h3>${planet.name}</h3>
                <div class="stat">${distance}</div>
            `;
            grid.appendChild(card);
        });
    }

    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', () => {
        const query = searchInput.value. toLowerCase();
        const filtered = allPlanets.filter(planet =>
            planet.name.toLowerCase().includes(query)
        );
        renderPlanets(filtered);
    });
        