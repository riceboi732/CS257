/*
 * Victor Huang, Martin Bernard
 */

window.onload = initialize;

function initialize(){
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '';
    
    var url = window.location.href;
    var state_id = url.substring(41)

    var apiUrl = baseURL + '/victims?state=' + state_id;
    console.log(apiUrl)

    fetch(apiUrl, {method: 'get'})

    .then((response) => response.json())
    
    .then(function(state) {
        var listBody = '';
        for (var k = 0; k < state.length; k++) {
            var victim = state[k]
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
}

function onFilter(){
    var min_year = document.getElementById('min_year').value;
    var max_year = document.getElementById('max_year').value; 

    var ethnicity = raceCheck();

    var arm = armedCheck();

    if (ethnicity === undefined){
        ethnicity = "all"
    }

    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '';

    var url = window.location.href;
    var state_id = url.substring(41)

    var apiUrl = baseURL + '/victims?state=' + state_id + '&ethnicity=' + ethnicity + '&armed=' + arm 
                    + '&min_year=' + min_year + '&max_year=' + max_year;
    console.log(apiUrl)
    fetch(apiUrl, {method: 'get'})

    .then((response) => response.json())
    
    .then(function(state) {
        var listBody = '';
        for (var k = 0; k < state.length; k++) {
            var victim = state[k]
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
}

function raceCheck(){
    var raceDict = {'african_american': "Black", 
                    'asian': "Asian", 'hispanic': "Hispanic", 'other': "Other"}
    var raceId = ['african_american', 'asian', 'hispanic', 'white', 'other']

    var checkedRace = "all"

    for(var i = 0; i < raceId.length; i++){
        if(document.getElementById(raceId[i]).checked){
            checkedRace = raceId[i]
        }
    }

    if(raceDict[checkedRace] == undefined){
        return "all";
    }
    else{
        return raceDict[checkedRace]
    }
}

function armedCheck() {
    var armedId = ['armed', 'unarmed'];

    var checkedArm = 'all';

    for(var i = 0; i < armedId.length; i++){
        if(document.getElementById(armedId[i]).checked){
            checkedArm = armedId[i]
        }
    }
    console.log(checkedArm);
    return checkedArm; 
}

//* Implment Later
//  * webapp.js
//  * Victor Huang, Martin Bernard
//  */


// window.onload = initialize;

// // This is example data that gets used in the click-handler below. Also, the fillColor
// // specifies the color those states should be. There's also a default color specified
// // in the Datamap initializer below.
// var extraStateInfo = {
//     MN: {population: 5640000, jeffhaslivedthere: true, fillColor: '#2222aa'},
//     CA: {population: 39500000, jeffhaslivedthere: true, fillColor: '#2222aa'},
//     NM: {population: 2100000, jeffhaslivedthere: false, fillColor: '#2222aa'},
//     OH: {population: 0, jeffhaslivedthere: false, fillColor: '#aa2222'}
// };

// function initialize() {
//     initializeMap();
// }

// function initializeMap() {
//     var map = new Datamap({ element: document.getElementById('map-container'), // where in the HTML to put the map
//                             scope: 'usa', // which map?
//                             projection: 'equirectangular', // what map projection? 'mercator' is also an option
//                             done: onMapDone, // once the map is loaded, call this function
//                             data: extraStateInfo, // here's some data that will be used by the popup template
//                             fills: { defaultFill: '#999999' },
//                             geographyConfig: {
//                                 //popupOnHover: false, // You can disable the hover popup
//                                 //highlightOnHover: false, // You can disable the color change on hover
//                                 popupTemplate: hoverPopupTemplate, // call this to obtain the HTML for the hover popup
//                                 borderColor: '#eeeeee', // state/country border color
//                                 highlightFillColor: '#bbbbbb', // color when you hover on a state/country
//                                 highlightBorderColor: '#000000', // border color when you hover on a state/country
//                             }
//                           });
// }

// // This gets called once the map is drawn, so you can set various attributes like
// // state/country click-handlers, etc.
// function onMapDone(dataMap) {
//     dataMap.svg.selectAll('.datamaps-subunit').on('click', onStateClick);
// }

// function hoverPopupTemplate(geography, data) {
//     var population = 0;
//     if (data && 'population' in data) {
//         population = data.population;
//     }

//     var jeffHasLivedThere = 'No';
//     if (data && 'jeffhaslivedthere' in data && data.jeffhaslivedthere) {
//         jeffHasLivedThere = 'Yes';
//     }

//     var template = '<div class="hoverpopup"><strong>' + geography.properties.name + '</strong><br>\n'
//                     + '<strong>Population:</strong> ' + population + '<br>\n'
//                     + '<strong>Has Jeff lived there?</strong> ' + jeffHasLivedThere + '<br>\n'
//                     + '</div>';

//     return template;
// }

// function onStateClick(geography) {
//     // geography.properties.name will be the state/country name (e.g. 'Minnesota')
//     // geography.id will be the state/country name (e.g. 'MN')
//     var stateSummaryElement = document.getElementById('state-summary');
//     if (stateSummaryElement) {
//         var summary = '<p><strong>State:</strong> ' + geography.properties.name + '</p>\n'
//                     + '<p><strong>Abbreviation:</strong> ' + geography.id + '</p>\n';
//         if (geography.id in extraStateInfo) {
//             var info = extraStateInfo[geography.id];
//             summary += '<p><strong>Population:</strong> ' + info.population + '</p>\n';
//         }

//         stateSummaryElement.innerHTML = summary;
//     }
// }
