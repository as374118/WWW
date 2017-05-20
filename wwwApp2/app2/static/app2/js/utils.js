function createPageTitle(text) {
	return '<h1 id=\'pageTitle\'>' + text + '</h1';
}

function createTitle1(text) {
	return createElementInternal('h1', text);
}

function createTitle2(text) {
	return createElementInternal('h2', text);
}

function createTitle3(text) {
	return createElementInternal('h3', text);
}

function createTitle4(text) {
	return createElementInternal('h4', text);
}

function createTableHeader(text) {
	return createElementInternal('th', text);
}

function createTableCell(text) {
	return createElementInternal('td', text);
}

function createClickable(text) {
	return createElementInternal('a', text);
}

function createClickableV2(text, onClickValue) {
	return '<a onclick=\"' + onClickValue + '\">' + text + '</a>';
}

function createListPosition(text) {
	return createElementInternal('li', text);
}

function createListPositionClickable(text, onClickValue) {
	return createElementInternal('li', createClickableV2(text, onClickValue));
}

function createTableCellClickable(text, onClickValue) {
	return createElementInternal('td', createClickableV2(text, onClickValue));
}

function packFunction(functionName, args) {
	res = functionName + '(' + '\'';
	res += args;
	res += '\'' + ')';
	return res;
}

function createElementInternal(tag, text) {
	return '<' + tag + '>' + text + '</' + tag + '>';
}


function getCandidates(callback) {
	candidates = []
	$.getJSON('/app2/candidates_api', function(result){
		$.each(result, function(i, field){
			candidates.push(field);
		});
		callback();
	});
}

function getMainResult(callback) {
	mainResult = []
	$.getJSON('/app2/voivodeship_api', function(result) {
		$.each(result, function(i, field){
			mainResult.push(field);
		});
		callback();
	});
}

function getVoivodeshipResult(voivodeshipName, callback) {
	voivodeshipResult = []
	$.getJSON('/app2/voivodeship_api/?voivodeship=' + voivodeshipName, function(result) {
		$.each(result, function(i, field){
			voivodeshipResult.push(field);
		});
		callback();
	});
}

function getRegionResult(regionName, callback) {
	regionResult = []
	$.getJSON('/app2/region_api?region=' + regionName, function(result) {
		$.each(result, function(i, field){
			regionResult.push(field);
		});
		callback();
	});
}

function getBoroughResult(boroughName, callback) {
	boroughResult = []
	$.getJSON('/app2/borough_api?borough=' + borough, function(result) {
		$.each(result, function(i, field){
			boroughResult.push(field);
		});
		callback();
	});
}

function getUserName(callback) {
	$.getJSON('/app2/user_api', function(result) {
		userName = result[0];
		if (callback != null) {
			callback();
		}
	});
}

function isAuthorized() {
	getUserName();
	return userName != '';
}

function generateTable(data, leftColumnName, onClickFunction) {
	$('table.resultTable').empty();
	htmlToAppend = '';
	htmlToAppend += generateHeaders(leftColumnName);
	htmlToAppend += generateCells(data, onClickFunction);
	$('table.resultTable').append(htmlToAppend);
	$('table.resultTable').show(animationTime);
}

function generateHeaders(leftColumnName) {
	htmlToAppend = '<tr>' + createTableHeader(leftColumnName);
	$.each(candidates, function(i, item) {
		htmlToAppend += createTableHeader(item.name);
	});
	htmlToAppend += '</tr>';
	return htmlToAppend;
}

function generateCells(data, onClickFunction) {
	htmlToAppend = '';
	$.each(data, function(i, candResultsList) {
		leftColumnValue = candResultsList[0];
		onClickValue = packFunction(onClickFunction, leftColumnValue);
		htmlToAppend += '<tr>' + createTableCellClickable(leftColumnValue, onClickValue);
		$.each(candResultsList[1], function(j, candResult) {
			candidateName = candResult[0];
			result = candResult[1];
			htmlToAppend += createTableCell(result);
		});
		htmlToAppend += '</tr>';
	});
	return htmlToAppend;
}

function addSearchPanel() {
	bindSearchImage();
	addLoginPanel();
}

function addLoginPanel() {
	getUserName(function() {
		if (!isAuthorized()) {
			$('#loginPanel').html('Log in');
		} else {
			$('#loginPanel').html('Hi, ' + userName);
		}
	});
}

function bindSearchImage() {
	$('#searchImage').click(function() {
		$('#searchInput').show(animationTime);
		$('#searchInput').focus();
		bindGoSearch();
		bindFocusoutHidding();
	});	
}

function bindFocusoutHidding() {
	$('#searchInput').focusout(function() {
		if (!($('#searchImage').is(':hover'))) {
			$('#searchInput').val('');
			$('#searchInput').hide(animationTime);
		}
	});
}

function bindGoSearch() {
	$('#searchImage').click(function() {
		var text = $('#searchInput').val();
		if (text != '') {
			goSearch(text);
		}
	});
	$('#searchInput').keypress(function(e) {
		var key = e.which;
		var text = $('#searchInput').val();
		if (key == 13 && text != '') { // enter == 13
			goSearch(text);
		}
	});	
}

function goSearch(boroughName) {
	searchGenerate(boroughName);
}

function fillSearchResult(borough) {
	$.getJSON('/app2/borough_search_api?borough=' + borough, function(result) {
		if (result.length == 0) {
			$('#searchResultList').append(createListPosition('Niestety nic nie znalieziono :('));
			$('#searchResult').show(animationTime);
		} else {
			var htmlToAppend = '';
			$.each(result, function(i, field) {
				var onClickValue = packFunction('boroughGenerate', field);
				htmlToAppend += createListPositionClickable(field, onClickValue);
			});
			$('#searchResultList').append(htmlToAppend);
			$('#searchResult').show(animationTime);
		}
	});
}

function makeVotesClickable() {
	var headers = $('table.resultTable').find('th');
	$.each(headers, function(i, header) {
		if (header.textContent != 'Gmina') {
			makeVoteClickable(header);
		}
	})
}

function makeVoteClickable(header) {
	$(header).css('text-decoration', 'underline');
	var attr = borough + '\', \'' + header.textContent;
	var onClickValue = packFunction('editVoteGenerate', attr);
	$(header).attr('onclick', onClickValue);
}

function getVotes(boroughName, candidateName, callback) {
	res = 0;
	$.getJSON(
		'/app2/votes_api/?borough=' + boroughName + '&candidate=' + candidateName,
		function(result) {
			res = result[0].votes;
			callback(res);
		}
	);
	return res;
}