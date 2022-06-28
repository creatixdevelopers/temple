"use strict";

/***********************************************
 * TEMPLATE: COUNTDOWN
 ***********************************************/
(function ($) {
    'use strict'; // check if plugin defined

    if (typeof $.fn.countdown === 'undefined') {
        return;
    }

    VLTJS.countdown = {
        init: function init() {
            $('.countdown').each(function () {
                var $this = $(this),
                    dueDate = $this.data('due-date') || false;
                $this.countdown(dueDate, function (event) {
                    $this.find('[data-days]').html(event.strftime('%D'));
                    $this.find('[data-hours]').html(event.strftime('%H'));
                    $this.find('[data-minutes]').html(event.strftime('%M'));
                    $this.find('[data-seconds]').html(event.strftime('%S'));
                });
            });
        }
    };
    VLTJS.countdown.init();
})(jQuery);

$(document).ready(function () {

    var counters = $(".count");
    var countersQuantity = counters.length;
    var counter = [];

    for (var i = 0; i < countersQuantity; i++) {
        counter[i] = parseInt(counters[i].innerHTML);
    }

    var count = function (start, value, id) {
        var localStart = start;
        setInterval(function () {
            if (localStart < value) {
                localStart++;
                counters[id].innerHTML = localStart;
            }
        }, 200);
    }

    for (var j = 0; j < countersQuantity; j++) {
        count(0, counter[j], j);
    }
});