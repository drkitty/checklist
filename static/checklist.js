function forEach(collection, f) {
    for (var i = 0; i < collection.length; ++i)
        f(collection[i]);
};

function handle(selector, type, f) {
    forEach(document.querySelectorAll(selector), function(elem) {
        elem.addEventListener(type, function() { f(elem); });
    });
};

document.addEventListener('DOMContentLoaded', function() {
    handle('table#checklist td button.check', 'click', function(elem) {
        var done_text = '\u2611';
        var not_done_text = '\u2610';

        if (elem.innerHTML === done_text) {
            elem.innerHTML = not_done_text;
        } else {
            elem.innerHTML = done_text;
        };
    });
})
