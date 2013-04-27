var timespans = [
    { start: -7200, end: -1, title: 'last 2 hours' },
    { start: -21600, end: -1, title: 'last 6 hours' },
    { start: -86400, end: -1, title: 'last day' },
    { start: -259200, end: -1, title: 'last 3 days' },
    { start: -604800, end: -1, title: 'last week' },
    { start: -2678400, end: -1, title: 'last month' },
    { start: -8035200, end: -1, title: 'last 3 months' },
    { start: -16070400, end: -1, title: 'last 6 months' },
    { start: -31536000, end: -1, title: 'last year' },
];

function parse_qs(qs) {
    var dict = {};
    if (qs) {
        $.each(qs.split('&'), function(i, v){
          var pair = v.split('=');
          dict[pair[0]] = decodeURIComponent(pair[1]);
        });
    }
    return dict;
}

function encode_qs(dict) {
    var qs = '';
    for (var opt in dict) {
        if (qs != '')
            qs += '&';
        qs += opt + '=' + encodeURIComponent(dict[opt]);
    }
    return qs;
}

function timegraph_controls(controls, images) {
    var bits = images.attr('src').split('?');
    var dict = parse_qs(bits[1]);

    function date_to_offset(date) {
        var now = new Date();
        return Math.floor((date.getTime() - now.getTime()) / 1000);
    }

    function offset_to_date(offset) {
        var now = new Date();
        return new Date(now.getTime() + 1000 * offset);
    }

    // determine current values
    var start = dict['start'] ? parseInt(dict['start']) : -86400;
    var end = dict['end'] ? parseInt(dict['end']) : -1;

    var html = '<select class="timegraph-preset">';
    for (var i in timespans) {
        html += '<option value="' + i + '"';
        if (timespans[i].start == start)
            html += ' selected="selected"';
        html += '>' + timespans[i].title + '</option>';
    }
    html += '</select>';
    html += '<input class="timegraph-start" type="text" size="16"/>';
    html += '<input class="timegraph-end" type="text" size="16"/>';
    controls.html(html);

    var start_field = controls.find('input.timegraph-start');
    start_field.datetimepicker({
        dateFormat: 'dd/mm/yy',
        onSelect: function(dateText, inst) {
            var date = start_field.datetimepicker('getDate');
            update_image(images, {'start': date_to_offset(date)});
    }});
    start_field.datetimepicker('setDate', offset_to_date(start));

    var end_field = controls.find('input.timegraph-end');
    end_field.datetimepicker({
        dateFormat: 'dd/mm/yy',
        onSelect: function(dateText, inst) {
            var date = end_field.datetimepicker('getDate');
            update_image(images, {'end': date_to_offset(date)});
    }});
    end_field.datetimepicker('setDate', offset_to_date(end));

    var timespan = controls.find('select.timegraph-preset');
    timespan.change(function() {
        var i = parseInt(timespan.val());
        if (i >= 0 && i < timespans.length) {
            // update start / end
            start_field.datetimepicker('setDate', offset_to_date(timespans[i].start));
            end_field.datetimepicker('setDate', offset_to_end(timespans[i].end));

            // update images
            update_image(images, {
                'start': timespans[i].start,
                'end': timespans[i].end,
            });
        }
    });

}

function update_image(images, options) {
    images.each(function() {
        var image = $(this);
        var bits = image.attr('src').split('?');
        var dict = parse_qs(bits[1]);
        for (var opt in options)
            dict[opt] = options[opt];
        image.attr('src', bits[0] + '?' + encode_qs(dict));
    });
}

$('.timegraph-graphs img').click(function() {
    var overlay = $('#timegraph-overlay');
    if (!overlay.length) {
        $('body').append('<div id="timegraph-overlay"></div>');
        overlay = $('#timegraph-overlay');
    }

    var qs = $(this).attr('src').split('?')[1];
    var nvpair = parse_qs(qs);
    var title = nvpair['title'];

    var html = '<div class="modal">';
    html += '<div class="modal-header">';
    html += '<button aria-hidden="true" data-dismiss="modal" class="close" type="button">×</button>';
    html += '<h3>' + title + '</h3>';
    html += '</div>';
    html += '<div class="modal-body">';
    html += '<img width="640" height="420" src="' + $(this).attr('src') + '"/>';
    html += '<form class="timegraph-controls" style="margin: 10px 0 0"></form>';
    html += '</div>';
    html += '</div>';

    overlay.html(html);
    overlay.find('div.modal').modal().css({width: '670px', 'margin-left': '-335px'});
    overlay.find('div.modal-body').css({'max-height': '460px'});

    var image = overlay.find('img');
    timegraph_controls(overlay.find('form'), image);

    // Handle time-shifting using drags.
    var start_offset;
    image.load(function() {
        $(this).css('left', 0);
    });
    image.draggable({
        axis: 'x',
        start: function(event, ui) {
            start_offset = ui.offset;
        },
        stop: function(event, ui) {
            var dict = parse_qs(image.attr('src').split('?')[1]);
            var start = dict['start'] ? parseInt(dict['start']) : -86400;
            var end = dict['end'] ? parseInt(dict['end']) : -1;
            var width = parseInt(dict['width']);

            var time_offset = Math.min(-end-1, -Math.floor((ui.offset.left - start_offset.left) * (end - start) / width));
            update_image(image, {
                'start': start + time_offset,
                'end': end + time_offset});
        },
    });

    // Remove title and adjust image size.
    update_image(image, {
        'width': 640,
        'height': 420,
        'title': ''});
});

$('.timegraph-controls').each(function() {
    timegraph_controls($(this), $('.timegraph-graphs img'));
});
