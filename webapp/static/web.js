/*
 * webapp.js
 * Victor Huang, Martin Bernard
 */

window.onload = initialize;


function initialize() {
    initializeMap();
    var element = document.getElementById('minnesota_button');
    if (element) {
        element.onclick = onMinnesotaButton;
    }

    var element = document.getElementById('washington_button');
    if (element) {
        element.onclick = onWashingtonButton;
    }
}

function initializeMap() {
    var map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
                            scope: 'usa', // which map?
                            projection: 'equirectangular', // what map projection? 'mercator' is also an option
                            done: onMapDone, // once the map is loaded, call this function
                            data: extraStateInfo, // here's some data that will be used by the popup template
                            fills: { defaultFill: '#999999' },
                            geographyConfig: {
                                //popupOnHover: false, // You can disable the hover popup
                                //highlightOnHover: false, // You can disable the color change on hover
                                popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
                                borderColor: '#eeeeee', // state/country border color
                                highlightFillColor: '#bbbbbb', // color when you hover on a state/country
                                highlightBorderColor: '#000000', // border color when you hover on a state/country
                            }
                          });
}

function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick);
}

function hoverPopupTemplate(geography, data) {
    var population = 0;
    if (data && 'population' in data) {
        population = data.population;
    }

    var jeffHasLivedThere = 'No';
    if (data && 'jeffhaslivedthere' in data && data.jeffhaslivedthere) {
        jeffHasLivedThere = 'Yes';
    }

    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
                    + '<strong>Population:</strong> ' + population + '<br>\n'
                    + '<strong>Has Jeff lived there?</strong> ' + jeffHasLivedThere + '<br>\n'
                    + '</div>';

    return template;
}

function onStateClick(geography) {
    var stateSummaryElement = document.getElementById('state-summary');
    if (stateSummaryElement) {
        var summary = '<p><strong>State:</strong> ' + geography.properties.name + '</p>\n'
                    + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
        if (geography.id in extraStateInfo) {
            var info = extraStateInfo[geography.id];
            summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
        }

        stateSummaryElement.innerHTML = summary;
    }
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '';
    return baseURL;
}

function onMinnesotaButton() {
    var url = getAPIBaseURL() + '/victims?state=MN';
    console.log(url)
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
    var url = getAPIBaseURL() + '/victims?state=WA';

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