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
                return choices[i].bind(elem, selector)();
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
        elem.addEventListener(type, f.bind(elem));
    }

    forEach($$(selector), handler);

    return handler;
}

function parse(s) {
    t = document.createElement('template');
    t.innerHTML = s;
    return document.importNode(t.content.firstChild, true);
}
