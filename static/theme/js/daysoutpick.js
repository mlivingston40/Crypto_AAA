/*
 jQuery for form w/ one stock

 */

		// AUTO COMPLETE
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
    var url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=DUVWLU2beNviTCCvLch1&qopts.columns=ticker&date=' + date;
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
        var str = JSON.stringify(response)
        // convert data to JSON object
        var tickersObject = JSON.parse(str);
        // console.log( tickersObject )
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
        $("#ticker").easyAutocomplete(Tickers)
      },
    });
  });


// JS for Date updating for single stock and flash min start date after clicking on calendar start date
var from_default = moment().subtract(2, 'years')
var from_max = moment().subtract(90, 'days')

var to_default = moment().subtract(1, 'days')
var to_max = moment().subtract(1, 'days')


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
  $('#date_end').data("DateTimePicker").minDate(e.date.add(90, 'days'));
});
$("#date_end").on("dp.change", function(e) {
  $('#date_start').data("DateTimePicker").maxDate(e.date.subtract(90, 'days'));
});



  $("#date_start").click(function() {

    var stock1 = $("#ticker").val();

    var yql_url = 'https://query.yahooapis.com/v1/public/yql';
    var url = 'https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?api_key=DUVWLU2beNviTCCvLch1&qopts.columns=date&ticker=' + stock1;
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

        var mindate = Tickers[0];

        $('#date_start').data("DateTimePicker").minDate(mindate);

        $('#date_end').data("DateTimePicker").minDate(mindate);

        $("#data").text(stock1 + " " + "data starts at" + " " + mindate).fadeIn();
        $("#data").fadeOut(5000);


      },
    });

  });

