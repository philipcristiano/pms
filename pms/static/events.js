var last_id = '000000000000000000000000';
$(function (){

    function event_to_str(event) {
        var string = '<div class="event accordian ' + event['_id'] + '"><p>';
        string += '<h3>' + event['time'] + '</h3>';
        for (key in event) {
            string += key + ': ' + event[key] + '<br>';
        }
        string += '<p></div>';
        return string
    }

    function insert_list() {
        $.getJSON('/list', {}, function(data) {
            var events = data['events'];
            last_id = events[0]['_id'];
            for(var i=0; i < events.length; i++){
                var event = events[i];
                $('#events').append(event_to_str(event));
            }
        });
    }

    function get_next_event() {
        var url = '/next/' + last_id;
        $.getJSON(url, {}, function(data) {
            if ('_id' in data) {
                last_id = data['_id'];
                $('#events').prepend(event_to_str(data));
                t = setTimeout(get_next_event, 1);
            }
            else {
                t = setTimeout(get_next_event, 1000);
            }
        });

    }
    get_next_event();

});
