/*
 * Victor Huang, Martin Bernard
 */

window.onload = initialize;

function initialize(){
    const wrapper = document.getElementById('state_button_container');
    if (wrapper != null) {
        wrapper.addEventListener('click', (event) => {
            if (event.target.className === 'stateButton'){
                var template = getAPIBaseURL() + '/victims.html?state=' + event.target.id; 
                
                window.location.assign(template);
            }
        })
    }
    initializeMap();
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '';
    return baseURL;
}

function initializeMap(){
    var map = new Datamap({ element: document.getElementById('map-container'),
                            scope: 'usa',
                            projection: 'equirectangular',
                            done: onMapDone,
                            fills: { defaultFill: '#00FFFF' },
                            geographyConfig: {
                                //popupOnHover: false,
                                //highlightOnHover: false,
                                popupTemplate: hoverPopupTemplate,
                                borderColor: '#eeeeee',
                                highlightFillColor: '#bbbbbb',
                                highlightBorderColor: '#000000',
                            }
                            });
}

function onMapDone(dataMap) {
    dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick)
}

function hoverPopupTemplate(geography) {
    var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n';

    return template;
}

function onStateClick(geography) {
    //geography.properties.name will be the state/country name (e.g. 'Minnesota')
    //geography.id will be the state/country name (e.g. 'MN')
    var template = getAPIBaseURL() + '/victims.html?state=' + geography.id
    window.location.assign(template);
    
}