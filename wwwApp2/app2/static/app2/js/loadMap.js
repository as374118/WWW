google.load('visualization', '1', {'packages': ['geochart']});
google.charts.load('current', {'packages':['corechart']});
google.setOnLoadCallback(drawMarkersMap);

function drawMarkersMap() {
	var data = new google.visualization.arrayToDataTable([['Województwo'], ['DOLNOŚLĄSKIE'], ['KUJAWSKO-POMORSKIE'], ['LUBELSKIE'], ['LUBUSKIE'], ['ŁÓDZKIE'], ['MAŁOPOLSKIE'], ['MAZOWIECKIE'], ['OPOLSKIE'], ['PODKARPACKIE'], ['PODLASKIE'], ['POMORSKIE'], ['ŚLĄSKIE'], ['ŚWIĘTOKRZYSKIE'], ['WARMIŃSKO-MAZURSKIE'], ['WIELKOPOLSKIE'], ['ZACHODNIOPOMORSKIE']]);
	var options = {
		region: 'PL',
		dataMode: 'regions',
		displayMode: 'regions',
		resolution: 'provinces',
		legend: 'none',
		enableRegionInteractivity: 'true',
		sizeAxis: {minSize: 5,  maxSize: 5},
		colorAxis: {colors: ['#0B2762']}
	};
	var chart = new google.visualization.GeoChart(document.getElementById('mapClickable'));
	google.visualization.events.addListener(chart, 'select', function () {
		var selection = chart.getSelection();
		if (selection.length > 0) {
			window.location = '/app2/voivodeship/' + data.getValue(selection[0].row, 0);
		}
	});
	chart.draw(data, options);
}