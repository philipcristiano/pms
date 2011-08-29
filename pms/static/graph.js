$(function start_graph() {
    var rollup_type = 'host-level';
    var number_of_days = '1';
    var rollup_props = $("#rollup_props");

    $("#rollup_select").change(function (argument) {
        rollup_type = $("#rollup_select option:selected").text();
        rollup_props.empty();
        update();
    });
    $("#days_select").change(function( argument) {
        number_of_days = $("#days_select option:selected").text();
        update();
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

        if (item) {
            $("#x").text(pos.x.toFixed(2));
            $("#y").text(pos.y.toFixed(2));
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
    properties_selection = {};

    function handle_prop_select_change() {
        properties_selection = {}
        $('.prop_select_box option:selected').each(function(){
            var type_name = $(this).attr('class');
            var type_value = $(this).text();
            if (!(type_name in properties_selection)){
                properties_selection[type_name] = [];
            }
            properties_selection[type_name].push(type_value)
        })
    }

    function prepare_prop_type_value(type, value) {
        // Ensures the type and value have the type and value
        var selector_id = "prop_select_" + type;
        var selector_item_id = selector_id + '_value_' + value;
        var select_box = $('#' + selector_id)
        if (select_box.length == 0) {
            var select_box_text = '<select multiple class="prop_select_box" id="'
                select_box_text += selector_id
                select_box_text += '" size=5></select>'
            rollup_props.append(select_box_text);
            select_box = $('#' + selector_id);
            select_box.change(handle_prop_select_change)

        }
        var select_box_item = $('#' +  selector_item_id);
        if (select_box_item.length == 0) {
            var select_item_text = '<option selected value="' + value + '" id="'
                select_item_text += selector_item_id +'"'
                select_item_text += ' class="' + type
                select_item_text += '">' + value + '</option>'
            select_box.append(select_item_text);
            select_box_item = $('#' +  selector_item_id);
            select_box_item.pms_type = type

        }
        select_box.change();

    }

    function update_rollup_props(rollups) {
        for (var i=0; i < rollups.length; i++){
            var rollup = rollups[i];
            for ( prop_type in rollup.pms_properties ) {
                var prop_value = rollup.pms_properties[prop_type];
                prepare_prop_type_value(prop_type, prop_value);
            }
        }
    }

    function get_selected_data(rollups) {
        var to_return = [];
        for (var i=0; i < rollups.length; i++){
            var rollup = rollups[i];
            rollup.failed = false;
            for (property in properties_selection){
                var value = rollup.pms_properties[property]
                var acceptable_values = properties_selection[property]
                if(jQuery.inArray(value, acceptable_values) == -1)
                    rollup.failed = true
            }
            if (!rollup.failed)
                to_return.push(rollup);
        }

        return to_return;
    }

    function update() {
        var hours = parseInt(number_of_days) * 24;
        url = '/rollup/latest/' + rollup_type + '/hourly/' + hours;
        $.getJSON(url, {}, function(data){
            update_rollup_props(data['response']);
            var drawable_data = get_selected_data(data['response']);
            plot.setData(drawable_data);
            plot.setupGrid();
            plot.draw();
            $('#last_updated').text(new Date().toString());
        });
    }
    function repeated_update(){
        update();
        setTimeout(repeated_update, 2000);
    }

    t = setTimeout(repeated_update, 1000);
    });
