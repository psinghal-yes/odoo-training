import json

from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class EstateAPI(http.Controller):
    @http.route('/properties',type='http',auth="public",methods=['GET'])
    def get_properties(self):
        _logger.info("*******  Inside controller function  *******")
        properties = request.env['estate.property'].sudo().search([])
        _logger.info("*****  Fetched %s properties from DB************", len(properties))
        data = []
        for p in properties:
            data.append({
                'id': p.id,
                'name': p.name,
                'price': p.expected_price,
                'state': p.state,
            })
        _logger.info("****** Returning %s properties ****************", len(data))

        return request.make_response(json.dumps(data))