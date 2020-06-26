function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
}

var config = {responsive: true}

var layout = {
    title: 'CDI',
    xaxis: {
        autorange: true,
        type: 'date'
    },
    yaxis: {
        autorange: true,
        type: 'linear'
    }
};

$.get('/api?investmentDate=2016-11-14&currentDate=2016-12-26&cdbRate=103.5', function(data) {
    var line = {
        type: 'scatter',
        mode: 'lines',
        x: unpack(data, 'date'),
        y: unpack(data, 'unitPrice'),
        line: {color: '#17BECF'}
    }

    var values = [line];

    Plotly.newPlot('chart', values, layout, config);
});

$('#update').click(function() {
    var data = {
        'currentDate': $('input[name$="currentDate"]').val(),
        'investmentDate': $('input[name$="investmentDate"]').val(),
        'cdbRate': $('input[name$="cdbRate"]').val(),
    };

    $.get('/api', data, function (data) {

        var line = {
            type: 'scatter',
            mode: 'lines',
            x: unpack(data, 'date'),
            y: unpack(data, 'unitPrice'),
            line: {color: '#17BECF'}
        };

        var values = [line];

        Plotly.newPlot('chart', values, layout, config);
    });
})