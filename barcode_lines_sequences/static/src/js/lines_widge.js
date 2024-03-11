odoo.define('barcode_lines_sequencesLinesWidget', function (require) {
    "use strict";

    var linesWidget = require('stock_barcode.LinesWidget');

    linesWidget.include({
        getProductLines: function (lines) {
            if (this.model === 'stock.inventory') {
                return this._sortProductLines(lines);
            }
            return this._super.apply(this, arguments);
        },

        /**
        * @override
        */
        _sortProductLines: function (lines) {
            return lines.sort(function(a,b) {
                return b.id - a.id
            });
        },
    })
})