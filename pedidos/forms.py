from django import forms


class ComprobantePagoForm(forms.Form):
    comprobante_pago = forms.ImageField(label='Sube tu comprobante de pago', required=True)
