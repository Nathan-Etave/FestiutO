function decrementBillet(element, idB) {
    element.onclick = void(0);
    fetch('/decrementer-billet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            idB: idB
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data[0] == '-1') {
            location.reload();
            return;
        }
        let totalElement = element.getRootNode().querySelector('#total');
        let currentTotal = parseFloat(totalElement.innerHTML.replace(' €', ''));
        if (data[0][0] == '0') {
            element.nextElementSibling.innerHTML = data[0][0];
            element.nextElementSibling.nextElementSibling.onclick = function() {incrementNewBillet(this, data[2], data[3], data[4], data[5], data[1])};
            element.parentNode.nextElementSibling.innerHTML = 'sous-total: ' + data[0][0] * data[1] + ' €';
            totalElement.innerHTML = (currentTotal - data[1]) + ' €';
        }
        else {
            element.nextElementSibling.innerHTML = data[0][0];
            element.nextElementSibling.nextElementSibling.onclick = function() {incrementBillet(this, data[0][1])};
            element.parentNode.nextElementSibling.innerHTML = 'sous-total: ' + data[0][0] * data[1] + ' €';
            totalElement.innerHTML = (currentTotal - data[1]) + ' €';
            element.onclick = function() {decrementBillet(this, data[0][1])};
        }
    });
}

function incrementBillet(element, idB) {
    element.onclick = void(0);
    fetch('/incrementer-billet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            idB: idB
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data[0] == '-1') {
            location.reload();
            return;
        }
        element.previousElementSibling.innerHTML = data[0][0];
        element.parentNode.nextElementSibling.innerHTML = 'sous-total: ' + data[0][0] * data[1] + ' €';
        let totalElement = element.getRootNode().querySelector('#total');
        let currentTotal = parseFloat(totalElement.innerHTML.replace(' €', ''));
        totalElement.innerHTML = (currentTotal + data[1]) + ' €';
        element.previousElementSibling.previousElementSibling.onclick = function() {decrementBillet(this, idB)};
        element.onclick = function() {incrementBillet(this, data[0][1])};
    });
}

function incrementNewBillet(element, idT, idU, dateD, dateF) {
    element.onclick = void(0);
    fetch('/incrementer-nouveau-billet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            idT: idT,
            idU: idU,
            dateD: dateD,
            dateF: dateF
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data[0] == '-1') {
            location.reload();
            return;
        }
        element.previousElementSibling.innerHTML = data[0][0];
        element.parentNode.nextElementSibling.innerHTML = 'sous-total: ' + data[0][0] * data[1] + ' €';
        let totalElement = element.getRootNode().querySelector('#total');
        let currentTotal = parseFloat(totalElement.innerHTML.replace(' €', ''));
        totalElement.innerHTML = (currentTotal + data[1]) + ' €';
        element.previousElementSibling.previousElementSibling.onclick = function() {decrementBillet(this, data[0][1])};
        element.onclick = function() {incrementBillet(this, data[0][1])};
    });
}