document.addEventListener('DOMContentLoaded', function() {
    var searchForm = document.getElementsByTagName('form')[0];
    var cards_container = document.getElementsByClassName('cards-content')[0];

    function handleEvent(event) {
        event.preventDefault();
        fetch('/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'search_term': document.getElementById('search').value
            })
        })
        .then(response => response.json())
        .then(data => {
            cards_container.innerHTML = '';
            Array.from(data).forEach(function(element) {
                var cardHTML = `
                <a href="/groupe/${element['groupe']['idG']}" id="${element['concert']['idC']}">
                    <div class="card">
                        <h3>${element['groupe']['nomG']}</h3>
                        <div class="date">
                            <p>${element['concert']['dateDebC']}</p>
                            <div><span></span></div>
                            <p>${element['concert']['dateFinC']}</p>
                        </div>
                        <p>${element['stylemusical']['nomS']}</p>
                    </div>
                </a>
            `;
            cards_container.innerHTML += cardHTML;
            });
        });
    }

    searchForm.addEventListener('submit', handleEvent);
    searchForm.addEventListener('input', handleEvent);
});