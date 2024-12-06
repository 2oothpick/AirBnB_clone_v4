const amenity_checkbox = document.querySelectorAll('.amenity.checkbox');
const amenity_list = document.querySelector('.amenities > h4');

/* Show checked states */
state_obj = {};
const state_checkbox = document.querySelectorAll('.state.checkbox');
const state_list = document.querySelector('.locations > h4');
state_checkbox.forEach((value, index) => {
    value.addEventListener('change', () => {
        if (value.checked == true) {
            state_obj[value.getAttribute('data-id')] =
                value.getAttribute('data-name');
        } else {
            delete state_obj[value.getAttribute('data-id')];
        }
        state_list.textContent = Object.values(state_obj).join(', ');
        /* console.log(Object.values(state_obj)) */
    });
});

/* Show checked cities */
city_obj = {};
const city_checkbox = document.querySelectorAll('.city.checkbox');
city_checkbox.forEach((value, index) => {
    value.addEventListener('change', () => {
        if (value.checked == true) {
            city_obj[value.getAttribute('data-id')] =
                value.getAttribute('data-name');
        } else {
            delete city_obj[value.getAttribute('data-id')];
        }
        state_list.textContent = Object.values(city_obj).join(', ');
        /* console.log(Object.values(city_obj)) */
    });
});

/* Show checked amenities */
amenity_obj = {};
amenity_checkbox.forEach((value, index) => {
    value.addEventListener('change', () => {
        if (value.checked == true) {
            amenity_obj[value.getAttribute('data-id')] =
                value.getAttribute('data-name');
        } else {
            delete amenity_obj[value.getAttribute('data-id')];
        }
        amenity_list.textContent = Object.values(amenity_obj).join(', ');
    });
});

/* API Status */
const api_status = document.querySelector('div#api_status');

async function fetchAPIStatus() {
    const url = 'http://127.0.0.1:5001/api/v1/status/';
    const response = await fetch(url);
    const json = await response.json();
    return json;
}

fetchAPIStatus().then((data) => {
    if (data['status'] === 'OK') {
        api_status.classList.add('available');
    } else {
        api.status.classList.remove('available');
    }
});

/* Show all places via API */
const places_section = document.querySelector('section.places');

const places_url = 'http://127.0.0.1:5001/api/v1/places_search/';
fetch(places_url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({}),
})
    .then((response) => response.json())
    .then((data) => {
        for (place of data) {
            const article = document.createElement('article');
            article.innerHTML += `
            <div class="title_box">
                  <h2>
                    ${place.name} 
                    </h2>
                <div class="price_by_night">
                    $${place.price_by_night} 
                    </div>
                </div>
                <div class="information">
                  <div class="max_guest"> 
                    ${place.max_guest}
                    ${place.max_guest !== 1 ? ' Guests' : ' Guest'}
                    </div>
                    <div class="number_rooms">
                    ${place.number_rooms}
                    ${place.number_rooms !== 1 ? ' Bedrooms' : ' Bedroom'}
                    </div>
                    <div class="number_bathrooms">
                    ${place.number_bathrooms}
                    ${place.number_bathrooms !== 1 ? ' Bathrooms' : ' Bathroom'}
                    </div>
                </div>
                <div class="user">
                  <b>Owner:</b> first name last name
                </div>
                <div class="description"> 
                    ${place.description}
                </div>
                <div class='reviews' place_id="${place.id}">

                <h2>Reviews <span id='show'>Hide</span> </h2>

                </div>
            `;
            places_section.appendChild(article);
        }

        /* Show reviews */
        const reviews_div = document.querySelectorAll('div.reviews');
        reviews_div.forEach((value, index) => {
            const place_id = value.getAttribute('place_id');

            async function fetchReviews() {
                const reviews_url = `http://127.0.0.1:5001/api/v1/places/${place_id}/reviews`;
                const response = await fetch(reviews_url);
                const json = await response.json();
                return json;
            }
            fetchReviews().then((data) => {
                const ul = document.createElement('ul');
                for (reviews of data) {
                    const li = document.createElement('li');
                    const h3 = document.createElement('h3');
                    const p = document.createElement('p');
                    h3.innerHTML = `from {person} {date}`;
                    p.innerHTML = `
                    Review: ${reviews['text']}`;
                    li.appendChild(h3);
                    li.appendChild(p);
                    /* console.log(place_id); */
                    ul.appendChild(li);
                }
                value.appendChild(ul);
            });
            /* show or hide reviews */
            const showSpan = document.querySelectorAll('span#show');
            showSpan[index].addEventListener('click', () => {
                async function showHide() {
                    const review_ul = document.querySelectorAll('.reviews>ul');
                    for (revValue of review_ul) {
                        const review_ulPlace_id =
                            revValue.parentNode.getAttribute('place_id');
                        const showSpanPlace_id =
                            showSpan[index].parentNode.parentNode.getAttribute(
                                'place_id',
                            );

                        if (showSpan[index].textContent == 'Hide') {
                            if (review_ulPlace_id == place_id) {
                                showSpan[index].textContent = 'Show';
                                //console.log(review_ul[index])
                                //review_ul[index].remove()
                                //console.log(review_ulPlace_id, place_id);
                                revValue.parentNode.removeChild(revValue);
                                break;
                            }
                        } else if (showSpan[index].textContent == 'Show') {
                            //console.log(review_ulPlace_id, place_id);
                            if (showSpanPlace_id == place_id) {
                                showSpan[index].textContent = 'Hide';
                                //console.log(review_ul[index])
                                fetchReviews().then((data) => {
                                    const ul = document.createElement('ul');
                                    for (reviews of data) {
                                        const li = document.createElement('li');
                                        const h3 = document.createElement('h3');
                                        const p = document.createElement('p');
                                        h3.innerHTML = `from {person} {date}`;
                                        p.innerHTML = `
                                                Review: ${reviews['text']}`;
                                        li.appendChild(h3);
                                        li.appendChild(p);

                                        ul.appendChild(li);
                                    }
                                    value.appendChild(ul);
                                });
                            }
                        }
                    }
                }
                showHide();
            });
        });
    });

/* Filter places */
const search_button = document.querySelector('button');

search_button.addEventListener('click', () => {
    places_section.innerHTML = '';

    const places_url = 'http://127.0.0.1:5001/api/v1/places_search/';
    fetch(places_url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: Object.keys(amenity_obj).length
            ? JSON.stringify({
                  amenities: Object.keys(amenity_obj),
                  states: Object.keys(state_obj),
                  cities: Object.keys(city_obj),
              })
            : JSON.stringify({}),
    })
        .then((response) => response.json())
        .then((data) => {
            /* console.log(data.length) */
            for (place of data) {
                const article = document.createElement('article');
                article.innerHTML += `
            <div class="title_box">
                  <h2>
                    ${place.name} 
                    </h2>
                <div class="price_by_night">
                    $${place.price_by_night} 
                    </div>
                </div>
                <div class="information">
                  <div class="max_guest"> 
                    ${place.max_guest}
                    ${place.max_guest !== 1 ? ' Guests' : ' Guest'}
                    </div>
                    <div class="number_rooms">
                    ${place.number_rooms}
                    ${place.number_rooms !== 1 ? ' Bedrooms' : ' Bedroom'}
                    </div>
                    <div class="number_bathrooms">
                    ${place.number_bathrooms}
                    ${place.number_bathrooms !== 1 ? ' Bathrooms' : ' Bathroom'}
                    </div>
                </div>
                <div class="user">
                  <b>Owner:</b> first name last name
                </div>
                <div class="description"> 
                    ${place.description}
                </div>
                <div class='reviews' place_id="${place.id}">

                <h2>Reviews <span id='show'>Hide</span> </h2>

                </div>
            `;
                places_section.appendChild(article);
            }

            /* Show reviews */
            const reviews_div = document.querySelectorAll('div.reviews');
            reviews_div.forEach((value, index) => {
                const place_id = value.getAttribute('place_id');

                async function fetchReviews() {
                    const reviews_url = `http://127.0.0.1:5001/api/v1/places/${place_id}/reviews`;
                    const response = await fetch(reviews_url);
                    const json = await response.json();
                    return json;
                }
                fetchReviews().then((data) => {
                    const ul = document.createElement('ul');
                    for (reviews of data) {
                        const li = document.createElement('li');
                        const h3 = document.createElement('h3');
                        const p = document.createElement('p');
                        h3.innerHTML = `from {person} {date}`;
                        p.innerHTML = `
                    Review: ${reviews['text']}`;
                        li.appendChild(h3);
                        li.appendChild(p);
                        /* console.log(place_id); */
                        ul.appendChild(li);
                    }
                    value.appendChild(ul);
                });
                /* show or hide reviews */
                const showSpan = document.querySelectorAll('span#show');
                showSpan[index].addEventListener('click', () => {
                    async function showHide() {
                        const review_ul =
                            document.querySelectorAll('.reviews>ul');
                        for (revValue of review_ul) {
                            const review_ulPlace_id =
                                revValue.parentNode.getAttribute('place_id');
                            const showSpanPlace_id =
                                showSpan[
                                    index
                                ].parentNode.parentNode.getAttribute(
                                    'place_id',
                                );

                            if (showSpan[index].textContent == 'Hide') {
                                if (review_ulPlace_id == place_id) {
                                    showSpan[index].textContent = 'Show';
                                    //console.log(review_ul[index])
                                    //review_ul[index].remove()
                                    //console.log(review_ulPlace_id, place_id);
                                    revValue.parentNode.removeChild(revValue);
                                    break;
                                }
                            } else if (showSpan[index].textContent == 'Show') {
                                //console.log(review_ulPlace_id, place_id);
                                if (showSpanPlace_id == place_id) {
                                    showSpan[index].textContent = 'Hide';
                                    //console.log(review_ul[index])
                                    fetchReviews().then((data) => {
                                        const ul = document.createElement('ul');
                                        for (reviews of data) {
                                            const li =
                                                document.createElement('li');
                                            const h3 =
                                                document.createElement('h3');
                                            const p =
                                                document.createElement('p');
                                            h3.innerHTML = `from {person} {date}`;
                                            p.innerHTML = `
                                                Review: ${reviews['text']}`;
                                            li.appendChild(h3);
                                            li.appendChild(p);

                                            ul.appendChild(li);
                                        }
                                        value.appendChild(ul);
                                    });
                                }
                            }
                        }
                    }
                    showHide();
                });
            });
        });
});
