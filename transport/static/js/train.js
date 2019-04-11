// socket io namespace
namespace = '/train';

// connect to the socket io server
var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

// send a search request
function search() {
    socket.emit('search_event', {station: $('#search_data').val()});
    return false;
}

// receive a search result
socket.on( 'train_result', function( trains ) {
    var trainTable = document.getElementById("train_table")
    trainTable.innerHTML = ''
    var depart = JSON.parse(trains);

    //var stationName = document.getElementById("station_name")
    //stationName.innerText = ''
    //var stationText = document.createTextNode(live.station_name)
    //stationName.appendChild(stationText)

    //var depart = live.departures.all
    var trainCount = depart.length
    for (var i = 0; i < trainCount; i++) {
        var row = document.createElement("tr")
        if(depart[i].status === "CANCELLED") {
            row.setAttribute("class", "bg-danger")
        } else if (depart[i].status === "LATE") {
            row.setAttribute("class", "bg-warning")
        } else {
            row.setAttribute("class", "bg-success")
        }

        var aimedCell = document.createElement("td")
        var aimedText = document.createTextNode(depart[i].aimed_departure_time)
        aimedCell.appendChild(aimedText)
        row.appendChild(aimedCell)


        var expectedCell = document.createElement("td")
        var expectedText = document.createTextNode(depart[i].expected_departure_time)
        expectedCell.appendChild(expectedText)
        row.appendChild(expectedCell)

        var destCell = document.createElement("td")
        var destText = document.createTextNode(depart[i].destination_name)
        destCell.appendChild(destText)
        row.appendChild(destCell)

        var platCell = document.createElement("td")
        var platText = document.createTextNode(depart[i].platform)
        platCell.appendChild(platText)
        row.appendChild(platCell)

        var opCell = document.createElement("td")
        var opText = document.createTextNode(depart[i].operator_name)
        opCell.appendChild(opText)
        row.appendChild(opCell)

        var originCell = document.createElement("td")
        var originText = document.createTextNode(depart[i].origin_name)
        originCell.appendChild(originText)
        row.appendChild(originCell)

        var statusCell = document.createElement("td")
        var statusText = document.createTextNode(depart[i].status)
        statusCell.appendChild(statusText)
        row.appendChild(statusCell)

        trainTable.appendChild(row)
    }
})