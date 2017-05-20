window.onload = function() {
	// alert( 'Page generator OK!!!');
	start();
};

// current page type {main, voivodeship, region, borough, editVote, search}
var type;
var voivodeship, region, borough, candidate, userName
var candidates = [], mainResult = [], voivodeshipResult = [], regionResult = [], boroughResult = []
var animationTime = 500

function start() {
	$.getScript('/static/app2/js/utils.js', function() {
		preparePage();
		mainGenerate();
	});
}

function preparePage() {
	getUserName();
	addSearchPanel();
	$('#header').append(createPageTitle('Główna strona'));
	$('#returnToMain').html("<a>Wróć na główną</a>");
	$('#resultChart').remove();
	$('#mapClickable').css('margin: auto;');
	$('#returnToMain').click(function() {
		// location.reload();
		mainGenerate();
		return false;
	});
}

function cleanPage() {
	$('#searchResultList').empty();
	$('#searchResult').hide(animationTime);
	$('table.resultTable').hide(animationTime);
	$('table.resultTable').empty();
	$('#voteForm').hide(animationTime);

	var pageTitle = 'Główna strona';
	if (type == 'main') {
		pageTitle = 'Główna strona';
	} else
	if (type == 'voivodeship') {
		pageTitle = 'Województwo ' + voivodeship;
	} else
	if (type == 'region') {
		pageTitle = 'Okręg ' + region;
	} else
	if (type == 'borough') {
		pageTitle = 'Gmina ' + borough;
	} else
	if (type == 'editVote') {
		pageTitle = 'Edycja głosu';
	} else
	if (type == 'search') {
		pageTitle = 'Wyniki wyszukiwania dla: ' + borough;
	}
	$('#pageTitle').html(pageTitle);
}

function mainGenerate() {
	type = 'main';
	cleanPage();
	getCandidates(function() {
		getMainResult(function () {
			$('#mapClickable').show(animationTime);
			generateTable(mainResult, 'Województwo', 'voivodeshipGenerate');
		});
	});
}

function voivodeshipGenerate(voivodeshipName) {
	type = 'voivodeship';
	voivodeship = voivodeshipName;
	cleanPage();
	getCandidates(function() {
		getVoivodeshipResult(voivodeshipName, function () {
			$('#mapClickable').show(animationTime);
			generateTable(voivodeshipResult, 'Okręg', 'regionGenerate');
		});
	});
}

function regionGenerate(regionName) {
	type = 'region';
	region = regionName;
	cleanPage();
	getCandidates(function() {
		getRegionResult(regionName, function () {
			$('#mapClickable').show(animationTime);
			generateTable(regionResult, 'Gmina', 'boroughGenerate');
		});
	});
}

function boroughGenerate(boroughName) {
	type = 'borough';
	borough = boroughName;
	cleanPage();
	getCandidates(function() {
		getBoroughResult(boroughName, function () {
			$('#mapClickable').show(animationTime);
			generateTable(boroughResult, 'Gmina', 'boroughGenerate');
			makeVotesClickable();
		});
	});
}

function editVoteGenerate(boroughName, candidateName) {
	if (isAuthorized()) {
		getVotes(boroughName, candidateName, function(votes) {
			type = 'editVote';
			borough = boroughName;
			candidate = candidateName;
			cleanPage();
			$('#mapClickable').hide(animationTime);
			$('input[name=\'borough\']').val(boroughName);
			$('input[name=\'candidate\']').val(candidateName);
			$('input[name=\'votes\']').val(votes);
			$('#voteForm').show(animationTime);
		});
	} else {
		window.location = '/admin';
	}
}

//  TODO polepszyc funkcje
function addMessage(text) {
	alert(text);
}

function addError(text) {
	alert(text);
}

function editVotePost() {
	boroughName = borough;
	candidateName = candidate;
	votesNew = $('input[name=\'votes\']').val();
	$.post(
		'/app2/votes_api/',
		{ 'borough': boroughName, 'candidate': candidateName, 'votes': votesNew }
	).done(function(data) {
		console.log(data);
		mainGenerate();
		if (data['ERROR'] == null ) {
			addMessage('Pomyślnie ustawione głosy dla kandydata: ' + candidateName +
			'w gminie: ' + boroughName);
		} else {
			addError('Niestety wystąpił błąd' + data['ERROR']);
		}
	})
}

function searchGenerate(boroughName) {
	type = 'search';
	borough = boroughName;
	cleanPage();
	$('#mapClickable').show(animationTime);
	fillSearchResult(borough);
}
