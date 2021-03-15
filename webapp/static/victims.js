/*
 * Victor Huang, Martin Bernard
 */

window.onload = initialize;

function initialize(){
    var apiUrl = getAPIBaseURL() + '/victims?state=' + getStateId();
    console.log(apiUrl)

    fetch(apiUrl, {method: 'get'})

    .then((response) => response.json())
    
    .then(function(state) {
        var victimListElement = document.getElementById('victims_table');
        if (victimListElement) {
            victimListElement.innerHTML = makeTable(state);
        }
    })

    var state_name_element = document.getElementById('full_name');
    if (state_name_element){
        console.log(getStateId())
        state_name_element.innerHTML = getStateName(getStateId())
    }

    makeBread(); 

}

function getStateName(abbreviation){
    var state_dict = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
                      "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "DC": "District of Columbia",
                      "FL": "Florida", "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho","IL": "Illinois",
                      "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine",
                      "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
                      "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hempshire", "NJ": "New Jersey", "NM": "New Mexico", 
                      "NY": "New York", "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",  "OR": "Oregon",
                      "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
                      "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington", "WV": "West Virginia",
                      "WI": "Wisconsin", "WY": "Wyoming", "all": "United States"};
    
    return state_dict[abbreviation]; 
}

function getAPIBaseURL() {
    var baseURL = window.location.protocol + '//' + window.location.hostname + ':' + window.location.port + '';
    return baseURL;
}

function getStateId(){
    var url = window.location.href;
    var state_id = url.substring(41);

    return state_id; 
}

function onFilter(){
    var min_year = document.getElementById('min_year').value;
    var max_year = document.getElementById('max_year').value; 
    var min_age = document.getElementById('min_age').value;
    var max_age = document.getElementById('max_age').value; 

    var ethnicity = raceCheck();

    var arm = armedCheck();

    if (ethnicity === undefined){
        ethnicity = "all"
    }

    var apiUrl = getAPIBaseURL() + '/victims?state=' + getStateId() + '&ethnicity=' + ethnicity + '&armed=' + arm 
                    + '&min_year=' + min_year + '&max_year=' + max_year + '&min_age=' + min_age + '&max_age=' + max_age;
    console.log(apiUrl)
    fetch(apiUrl, {method: 'get'})

    .then((response) => response.json())
    
    .then(function(state) {
        if(makeTable(state) === "No Results. Please try another combination."){
            document.getElementById('victims_table').style.textAlign = "center"; 
        }
        var victimListElement = document.getElementById('victims_table');
        if (victimListElement) {
            victimListElement.innerHTML = makeTable(state);
        }
    })
}

function raceCheck(){
    var raceDict = {'african_american': "Black", 
                    'asian': "Asian", 'hispanic': "Hispanic", 'native': "Native", 'white': "White", 'other': "Other"}
    var raceId = ['african_american', 'asian', 'hispanic', 'native', 'white', 'other']

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

function makeTable(state){
    var titleRow = '<tr>\n' 
                    + '<th>' + 'Date' + '</th>\n'
                    + '<th>' + 'Name' + '</th>\n'
                    + '<th>' + 'Age' + '</th>\n'
                    + '<th>' + 'Gender' + '</th>\n'
                    + '<th>' + 'Ethnicity' + '</th>\n'
                    + '<th>' + 'Armed Status' + '</th>\n'
                    + '<th>' + 'State' + '</th>\n'
                    + '</tr>\n'
    var vicTable = '';
    console.log(state.length)
    if(state.length == 0){
        return "No Results. Please try another combination."
    }
    else{
        for (var k = 0; k < state.length; k++) {
            var victim = state[k]
            var ethnicity = victim['ethnicity']
            if(ethnicity == 'Black'){
                ethnicity = 'African American'
            }

            vicTable += '<tr>\n' + '<td>' 
                        + victim['date'] + '</td>\n'
                        + '<td>' + victim['name'] + '</td>\n'
                        + '<td>' + parseInt(victim['age'], 10) + '</td>\n'
                        + '<td>' + victim['gender'] + '</td>\n'
                        + '<td>' + ethnicity + '</td>\n'
                        + '<td>' + victim['armed'] + '</td>\n'
                        + '<td>' + victim['state'] + '</td>\n' + '</tr>\n';
        }

        return titleRow + vicTable 
    }
}

function onHome(){
    window.location.assign(getAPIBaseURL());
}

function onSearch(){
    var search_value = document.getElementById('search').value;
    
    var apiUrl = getAPIBaseURL() + '/victims?state=' + getStateId() + '&search=' + search_value; 
    console.log(apiUrl)
    fetch(apiUrl,{method: 'get'})

    .then((response) => response.json())

    .then(function(state){
        if(makeTable(state) === "No Results. Please try another combination."){
            document.getElementById('victims_table').style.textAlign = "center"; 
        }
        var victimTableElement = document.getElementById('victims_table');
        if(victimTableElement){
            victimTableElement.innerHTML = makeTable(state);
        }
    })
}

function makeBread(){
    var homeBread = '<a href=' + getAPIBaseURL() + '> Home</a>';

    var homeBreadButton = document.getElementById('home');
    if(homeBreadButton){
        homeBreadButton.innerHTML = homeBread;
    }

    var currPage = document.getElementById('cur_page');
    if(currPage){
        currPage.innerHTML = getStateName(getStateId())
    }
}