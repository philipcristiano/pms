$(function start_graph() {
    var rollup_type = 'host-level';

    $("#rollup_select").change(function (argument) {
        rollup_type = $("#rollup_select option:selected").text();
    });

    var options = {};
    var options2 = {
        xaxis: {mode: "time"},
        legend: {position: "nw"},
        grid: {hoverable: true, clickable: true},
        series: {
            lines: { show: true },
            points: { show: true }
        },
    };
    function showTooltip(x, y, contents) {
        $('<div id="tooltip">' + contents + '</div>').css( {
            position: 'absolute',
            display: 'none',
            top: y + 5,
            left: x + 5,
            border: '1px solid #fdd',
            padding: '2px',
            'background-color': '#fee',
            opacity: 0.80
        }).appendTo("body").fadeIn(200);
    }

    var previousPoint = null;
    $("#graph").bind("plothover", function (event, pos, item) {
        $("#x").text(pos.x.toFixed(2));
        $("#y").text(pos.y.toFixed(2));

        if (item) {
            if (previousPoint != item.dataIndex) {
                previousPoint = item.dataIndex;

                $("#tooltip").remove();
                var x = item.datapoint[0].toFixed(2),
                    y = item.datapoint[1].toFixed(2);

                showTooltip(item.pageX, item.pageY,
                            new Date(Math.floor(x)) + " = " + Math.floor(y));
            }
        }
        else {
            $("#tooltip").remove();
            previousPoint = null;
        }
    });
    $("#graph").bind("plotclick", function (event, pos, item) {
        $('#events').empty();
        if (item) {
            var d = Date(item.datapoint[0]);
            var query = item.series.pms_properties;

            query['pms_js_time'] = item.datapoint[0];
            $.getJSON('/query', query, function (data) {
                var events = data['events'];
                last_id = events[0]['_id'];
                for(var i=0; i < events.length; i++){
                    var event = events[i];
                    $('#events').append(event_to_str(event));
                }

            });
        }
    });

    var dummy_data = [];
    var d1 = [[0, 3], [4, 8], [8, 5], [9, 13]];
    var graph = $("#graph");
    var plot = $.plot(graph, [d1], options2);
    var t;
    function update() {
        url = '/rollup/latest/' + rollup_type + '/hourly/1';
        $.getJSON(url, {}, function(data){
            plot.setData(data['response']);
            plot.setupGrid();
            plot.draw();
            t = setTimeout(update, 2000);
        });
    }
    t = setTimeout(update, 1000);
    });
