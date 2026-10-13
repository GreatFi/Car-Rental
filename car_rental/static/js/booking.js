/* Booking: live estimate from the two date inputs.
   Expects .summary-lines[data-price] and #days-line/#days-label/#days-amount/#total. */

(function () {
    "use strict";

    var lines = document.querySelector(".summary-lines");
    if (!lines) return;

    var pricePerDay = parseFloat(lines.dataset.price);
    var daysLine = document.getElementById("days-line");
    var daysLabel = document.getElementById("days-label");
    var daysAmount = document.getElementById("days-amount");
    var total = document.getElementById("total");

    // Django's form fields render as type="date" — grab them in document order
    var dates = Array.prototype.slice.call(
        document.querySelectorAll('.booking-form input[type="date"]')
    );
    if (dates.length < 2) return;

    var startInput = dates[0];
    var endInput = dates[1];

    var naira = new Intl.NumberFormat("en-NG", {
        style: "currency",
        currency: "NGN",
        maximumFractionDigits: 0
    });

    function parseDate(value) {
        if (!value) return null;
        var parts = value.split("-");
        return new Date(+parts[0], +parts[1] - 1, +parts[2]);
    }

    function update() {
        var start = parseDate(startInput.value);
        var end = parseDate(endInput.value);

        // Keep the range sane: end can't be before start
        if (start) {
            var min = new Date(start);
            min.setDate(min.getDate() + 1);
            endInput.min = min.toISOString().slice(0, 10);
        }

        if (!start || !end || end <= start) {
            daysLine.hidden = true;
            total.textContent = "Select dates";
            return;
        }

        var days = Math.round((end - start) / 86400000);
        var amount = days * pricePerDay;

        daysLabel.textContent = days + " day" + (days === 1 ? "" : "s");
        daysAmount.textContent = "× " + naira.format(pricePerDay);
        daysLine.hidden = false;
        total.textContent = naira.format(amount);
    }

    startInput.addEventListener("change", update);
    endInput.addEventListener("change", update);
    update();
})();