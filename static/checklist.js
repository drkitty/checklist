var $ = document.querySelector.bind(document);
var $$ = document.querySelectorAll.bind(document);

function forEach(collection, f) {
    for (var i = 0; i < collection.length; ++i)
        f(collection[i]);
}

function handle(selector, type, f) {
    forEach($$(selector), function(elem) {
        elem.addEventListener(type, function() { f(elem); });
    });

    return function(elem) {
        elem.addEventListener(type, function() { f(elem); });
    };
}

function parse(s) {
    t = document.createElement('template');
    t.innerHTML = s;
    return document.importNode(t.content.firstChild, true);
}

function create_item(description) {
    data = new FormData();
    data.append('description', description);
    r = new XMLHttpRequest();
    r.onreadystatechange = function() {
        if (r.readyState == r.DONE) {
            if (r.status == 200) {
                console.log('Success!');
                container = $('#checklist-item-container');
                item = parse(r.responseText);
                item = container.insertBefore(item, null);
                handle_item(item.querySelector('button.check'));
            };
        };
    };
    r.open('POST', '/checklist/create');
    r.send(data);
}

var handle_item;

document.addEventListener('DOMContentLoaded', function() {
    handle_item = handle(
            '#checklist-item-container button.check', 'click', function(elem) {
        var done_text = '\u2611';
        var not_done_text = '\u2610';

        text_node = elem.childNodes[0];

        if (text_node.nodeValue == done_text) {
            text_node.nodeValue = not_done_text;
        } else {
            text_node.nodeValue = done_text;
        };
    });
})
