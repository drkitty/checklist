function getMatchesSelector() {
    choices = [
        Element.prototype.matches,
        Element.prototype.mozMatchesSelector,
        Element.prototype.webkitMatchesSelector,
        Element.prototype.msMatchesSelector,
        Element.prototype.oMatchesSelector,
    ];
    for (var i = 0; i <= choices.length - 1; ++i) {
        if (choices[i] !== undefined) {
            return function(elem, selector) {
                return choices[i].bind(elem, selector).call();
            };
        };
    };
}

var matchesSelector = getMatchesSelector();

var $ = document.querySelector.bind(document);
var $$ = document.querySelectorAll.bind(document);

function last(collection, i) {
    if (i === undefined)
        i = 1;
    return collection[collection.length - i];
}

// Search upward from `elem` for an element matched by `selector`.
function $up(elem, selector) {
    var target;
    while (elem = elem.parentElement) {
        if (matchesSelector(elem, selector)) {
            return elem;
        };
    };
    // Didn't find it: return undefined.
}

function forEach(collection, f) {
    for (var i = 0; i < collection.length; ++i)
        f(collection[i]);
}

function handle(selector, type, f) {
    handler = function(elem) {
        elem.addEventListener(type, function() { f(elem); });
    }

    forEach($$(selector), handler);

    return handler;
}

function parse(s) {
    t = document.createElement('template');
    t.innerHTML = s;
    return document.importNode(t.content.firstChild, true);
}

function create_item(description, callback) {
    data = new FormData();
    data.append('description', description);
    r = new XMLHttpRequest();
    r.onreadystatechange = function() {
        if (r.readyState == r.DONE) {
            if (r.status == 200) {
                container = $('#checklist-item-container');
                item = parse(r.responseText);
                item = container.insertBefore(
                    item, last(container.children));
                handle_remove(item.querySelector('button.remove-item'));
                handle_check(item.querySelector('button.check'));
                if (callback)
                    callback();
            };
        };
    };
    r.open('POST', '/create');
    r.send(data);
}

function remove_item(id, callback) {
    data = new FormData();
    data.append('id', id);
    r = new XMLHttpRequest();
    r.onreadystatechange = function() {
        if (r.readyState == r.DONE) {
            if (r.status == 204) {
                $('table#checklist tr[data-item-id="' + id + '"]').remove();
                if (callback)
                    callback;
            };
        };
    };
    r.open('POST', '/remove');
    r.send(data);
}

var handle_remove;
var handle_check;

document.addEventListener('DOMContentLoaded', function() {
    handle_remove = handle(
            'table#checklist button.remove-item', 'click', function(elem) {
        remove_item($up(elem, 'tr').getAttribute('data-item-id'));
    });

    handle_check = handle(
            'table#checklist button.check', 'click', function(elem) {
        var done_text = '\u2611';
        var not_done_text = '\u2610';

        text_node = elem.childNodes[0];

        if (text_node.nodeValue == done_text) {
            text_node.nodeValue = not_done_text;
        } else {
            text_node.nodeValue = done_text;
        };
    });

    handle('button#new-item', 'click', function(elem) {
        description_input = $('#new-item-container input[name=description]');
        description = description_input.value;
        if (description !== '') {
            create_item(description, function() {
                description_input.value = '';
            });
        };
    });
})
