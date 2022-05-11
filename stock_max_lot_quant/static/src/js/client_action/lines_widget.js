odoo.define('stock_barcode.MaxLotQuantWidget', function (require) {
'use strict';

var LinesWidget = require('stock_barcode.LinesWidget');
var rpc = require('web.rpc');


var MaxLotQuantWidget = LinesWidget.include({
    events: _.extend({}, LinesWidget.prototype.events, {
      'click .o_max_lots': '_onClickMaxLots',
    }),

    init: function (parent, page, pageIndex, nbPages) {
        this._super.apply(this, arguments);  // Always required inside monkey patched Odoo
//        this.display_action_record_components = parent.currentState.display_action_record_components;
    },


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
        ev.stopPropagation();
        var self_id = this.__parentedParent.actionParams.id;  // stock_picking.id = self.id
        this._maxlots(self_id);
    },

    _maxlots: function (id) {
        return rpc.query({
            model: 'stock.picking',
            method: 'button_max_lots',
            args: [[id]]
        }).then(data => {
            this.trigger_up('reload');
        });
    },

});

return MaxLotQuantWidget;

});