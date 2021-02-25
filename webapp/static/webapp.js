/*
 * webapp.js
 * Victor Huang Martin Bernard
 */

window.onload = initialize;

function initialize() {
    var element = document.getElementById('minnesota_button');
    if (element) {
        element.onclick = onMinnesotaButton;
    }

    var element = document.getElementById('washington_button');
    if (element) {
        element.onclick = onWashingtonButton;
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '/victims';
    return baseURL;
}

function onMinnesotaButton() {
    var url = getAPIBaseURL() + '?state=MN';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(minnesota) {
        var listBody = '';
        for (var k = 0; k < minnesota.length; k++) {
            var victim = minnesota[k];
            listBody += '<li>' + victim['date']
                      + ', ' + victim['name']
                      + ',' + victim['age']
                      + ', ' + victim['gender'];
                      + ', ' + victim['ethnicity'];
                      + ', ' + victim['armed'];
                      + ', ' + victim['state'];
                      + '</li>\n';
        }

        var victimListElement = document.getElementById('victims_list');
        if (victimListElement) {
            victimListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function onWashingtonButton() {
    var url = getAPIBaseURL() + '?state=WA';

    fetch(url, {method: 'get'})

    .then((response) => response.json())

    .then(function(washington) {
        var listBody = '';
        for (var k = 0; k < washington.length; k++) {
            var victim = washington[k];
            listBody += '<li>' + victim['date']
                      + ', ' + victim['name']
                      + ',' + victim['age']
                      + ', ' + victim['gender'];
                      + ', ' + victim['ethnicity'];
                      + ', ' + victim['armed'];
                      + ', ' + victim['state'];
                      + '</li>\n';
        }
        console.log(listBody)
        var victimListElement = document.getElementById('victims_list');
        if (victimListElement) {
            victimListElement.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

