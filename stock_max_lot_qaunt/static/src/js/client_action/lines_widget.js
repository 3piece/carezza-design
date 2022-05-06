odoo.define('stock_max_lot_qaunt.lines_widget', function (require) {
'use strict';

var LinesWidget = require('stock_barcode.LinesWidget');
var rpc = require('web.rpc');

/**
     * Makes the rpc to the validate method of the model.
     *
     * @private
     * @returns {Promise}
     */
//    _validate: function (context) {
//        return this._save().then(() => {
//            return this._rpc({
//                model: this.actionParams.model,
//                method: this.methods.validate,
//                context: context || {},
//                args: [[this.currentState.id]],
//            });
//        });
//    },

var MrpSubcontractingLinesWidget = LinesWidget.include({
    events: _.extend({}, LinesWidget.prototype.events, {
    'click .o_max_lots': '_onClickMaxLots',
    }),

    init: function (parent, page, pageIndex, nbPages) {
        this._super.apply(this, arguments);
        this.display_action_record_components = parent.currentState.display_action_record_components;
    },

    console.log("TEST 2");

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * Handles the click on the `Quality Checks` button.
     *
     * @private
     * @param {MouseEvent} ev
     */
     _onClickMaxLots: function (ev) {
     	debugger;
     	console.log("TEST");
//        /*ev.stopPropagation();*/
        var id = $(ev.target).parents('.o_barcode_line').data('id');
        return rpc.query({
                model: 'stock.move.line',
                method: 'unbuild_unit',
                kwargs: { 'sku_size' : 'inner','move_line_id':id},
            }).then(function (){console.log("TEST3")});
    }

});

return MrpSubcontractingLinesWidget;

});