from odoo import models, fields, api

class ServiceEstimate(models.Model):
    _name = 'service.estimate'
    _description = 'Service Estimate'

    name = fields.Char(string='Service Name', required=True)
    date = fields.Date(string='Date', required=True)
    total_material_cost = fields.Monetary(string='Total Material Cost', compute='_compute_total_material_cost', store=True, currency_field='currency_id')
    markup_percentage = fields.Float(string='Markup (%)', default=0.0)
    markup_value = fields.Monetary(string='Markup Value', compute='_compute_markup_value', store=True, currency_field='currency_id')
    wastage_percentage = fields.Float(string='Wastage (%)', default=0.0)
    wastage_value = fields.Monetary(string='Wastage Value', compute='_compute_wastage_value', store=True, currency_field='currency_id')
    total_cost = fields.Monetary(string='Total Estimate Cost', compute='_compute_total_cost', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    estimate_line_ids = fields.One2many('service.estimate.line', 'service_estimate_id', string='Estimate Lines')

    copies = fields.Integer(string='Copies', default=1)
    final_total_cost = fields.Monetary(string='Final Total Estimate Cost', compute='_compute_final_total_cost', store=True, currency_field='currency_id')

    @api.depends('estimate_line_ids.subtotal')
    def _compute_total_material_cost(self):
        for record in self:
            record.total_material_cost = sum(line.subtotal for line in record.estimate_line_ids)

    @api.depends('total_material_cost', 'markup_percentage')
    def _compute_markup_value(self):
        for record in self:
            record.markup_value = (record.markup_percentage / 100.0) * record.total_material_cost

    @api.depends('total_material_cost', 'wastage_percentage')
    def _compute_wastage_value(self):
        for record in self:
            record.wastage_value = (record.wastage_percentage / 100.0) * record.total_material_cost

    @api.depends('total_material_cost', 'markup_value', 'wastage_value')
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.total_material_cost + record.markup_value + record.wastage_value

    @api.depends('total_cost', 'copies')
    def _compute_final_total_cost(self):
        for record in self:
            record.final_total_cost = record.total_cost * record.copies

class ServiceEstimateLine(models.Model):
    _name = 'service.estimate.line'
    _description = 'Service Estimate Line'

    service_estimate_id = fields.Many2one('service.estimate', string='Service Estimate')
    material = fields.Char(string='Material')
    quantity = fields.Float(string='Quantity', required=True)
    unit_price = fields.Monetary(string='Unit Price', required=True, currency_field='currency_id')
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='service_estimate_id.currency_id', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

