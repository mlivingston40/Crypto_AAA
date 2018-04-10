/*
 jQuery for form w/ two stocks

 */
 		// AUTO COMPLETE for two stocks
function getPreviousWorkday() {
  let workday = moment();
  let day = workday.day();
  let diff = 1; // returns yesterday
  if (day == 0 || day == 1) { // is Sunday or Monday
    diff = day + 2; // returns Friday
  }
  return workday.subtract(diff, 'days');
}
$(function() {
  var yql_url = 'https://query.yahooapis.com/v1/public/yql';
  var today = getPreviousWorkday();
  var date = today.format('YYYY') + '-' + today.format('M') + '-' + today.format('D');
  var url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=-Sp4LKrbzSb5vuvP9KP6&qopts.columns=ticker&date=' + date;
  $.ajax({
    'url': yql_url,
    'data': {
      'q': 'SELECT * FROM json WHERE url="' + url + '"',
      'format': 'json',
      'jsonCompat': 'new',
    },
    'dataType': 'jsonp',
    'success': function(response) {
      // console.log(response);
      // console.log(JSON.stringify(response));
      var str = JSON.stringify(response);


      // convert data to JSON object
      var tickersObject = JSON.parse(str);
      // console.log( tickersObject );


      // empty array
      var tickersArray = [];
      // push nested data in JSON object to empty array
      $.each(tickersObject.query.results.json.datatable.data, function(index, value) {
        tickersArray.push(value.json);
      });
      // console.log(tickersArray);
      var Tickers = [];
      for (var key in tickersArray) {
        Tickers = Tickers.concat(tickersArray[key]);
      };
      var Tickers = {
        data: Tickers,
        theme: "plate-dark",
        list: {
          maxNumberOfElements: 10,
          match: {
            enabled: true
          }
        }
      };
      // console.log(Tickers);
      $("#ticker1").easyAutocomplete(Tickers);
      $("#ticker2").easyAutocomplete(Tickers);

    },
  });
});


// JS for Date updating for two stocks and flash min start date after clicking on calendar start date

var from_default = moment().subtract(1, 'years')
var from_max = moment().subtract(7, 'days')

var to_default = moment().subtract(1, 'days')
var to_max = moment().subtract(1, 'days')

var value1 = null;
var value2 = null;

$("#date_start").click(function() {
  var stock1 = $("#ticker1").val();

  var yql_url = 'https://query.yahooapis.com/v1/public/yql';
  var url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=-Sp4LKrbzSb5vuvP9KP6&qopts.columns=date&ticker=' + stock1;
  $.ajax({
    'url': yql_url,
    'data': {
      'q': 'SELECT * FROM json WHERE url="' + url + '"',
      'format': 'json',
      'jsonCompat': 'new',
    },
    'dataType': 'jsonp',
    'success': function(response) {
      // console.log(response);
      // console.log(JSON.stringify(response));
      var str = JSON.stringify(response);


      // convert data to JSON object
      var tickersObject = JSON.parse(str);
      // console.log( tickersObject );


      // empty array
      var tickersArray = [];
      // push nested data in JSON object to empty array
      $.each(tickersObject.query.results.json.datatable.data, function(index, value) {
        tickersArray.push(value.json);
      });
      //						  console.log(tickersArray);
      var Tickers = [];
      for (var key in tickersArray) {
        Tickers = Tickers.concat(tickersArray[key]);
      };
      //			 console.log(Tickers);

      var minDate = Tickers[0];

      $("#data1").text(stock1+" "+"data starts at"+" "+minDate).fadeIn();
      $("#data1").fadeOut(5000);

      ajaxCallBack1(minDate);
    },
  });
});

$("#date_start").click(function() {
  var stock2 = $("#ticker2").val();

  var yql_url = 'https://query.yahooapis.com/v1/public/yql';
  var url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=-Sp4LKrbzSb5vuvP9KP6&qopts.columns=date&ticker=' + stock2;
  $.ajax({
    'url': yql_url,
    'data': {
      'q': 'SELECT * FROM json WHERE url="' + url + '"',
      'format': 'json',
      'jsonCompat': 'new',
    },
    'dataType': 'jsonp',
    'success': function(response) {
      // console.log(response);
      // console.log(JSON.stringify(response));
      var str = JSON.stringify(response);


      // convert data to JSON object
      var tickersObject = JSON.parse(str);
      // console.log( tickersObject );


      // empty array
      var tickersArray = [];
      // push nested data in JSON object to empty array
      $.each(tickersObject.query.results.json.datatable.data, function(index, value) {
        tickersArray.push(value.json);
      });
      //						  console.log(tickersArray);
      var Tickers = [];
      for (var key in tickersArray) {
        Tickers = Tickers.concat(tickersArray[key]);
      };
      //			 console.log(Tickers);

      var minDate = Tickers[0];

      $("#data2").text(stock2+" "+"data starts at"+" "+minDate).fadeIn();
      $("#data2").fadeOut(5000);

      ajaxCallBack2(minDate);

    },
  });
});


function ajaxCallBack1(min1) {
  value1 = min1;

  var dates = [];
  dates.push(new Date(value1))
  dates.push(new Date(value2))

  var maxDate = new Date(Math.max.apply(null, dates));

  var minoverlap = maxDate.getUTCFullYear() + '-' + (maxDate.getUTCMonth() + 1) + '-' + maxDate.getUTCDate();

  $('#date_start').data("DateTimePicker").minDate(minoverlap);
  $('#date_end').data("DateTimePicker").minDate(minoverlap);
}

function ajaxCallBack2(min2) {
  value2 = min2;

  var dates = [];
  dates.push(new Date(value2))
  dates.push(new Date(value1))

  var maxDate = new Date(Math.max.apply(null, dates));

  var minoverlap = maxDate.getUTCFullYear() + '-' + (maxDate.getUTCMonth() + 1) + '-' + maxDate.getUTCDate();

  $('#date_start').data("DateTimePicker").minDate(minoverlap);
  $('#date_end').data("DateTimePicker").minDate(minoverlap);
}


$('#date_start').datetimepicker({
  useCurrent: false,
  format: 'YYYY-MM-DD',
  daysOfWeekDisabled: [0, 6],
  maxDate: from_max,
  defaultDate: from_default
});
$('#date_end').datetimepicker({
  useCurrent: false,
  format: 'YYYY-MM-DD',
  daysOfWeekDisabled: [0, 6],
    //minDate: from_default
   maxDate: to_max,
   defaultDate: to_default
});
$("#date_start").on("dp.change", function(e) {
  $('#date_end').data("DateTimePicker").minDate(e.date.add(7, 'days'));
});
$("#date_end").on("dp.change", function(e) {
  $('#date_start').data("DateTimePicker").maxDate(e.date.subtract(7, 'days'));
});


