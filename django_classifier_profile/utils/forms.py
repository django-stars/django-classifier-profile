class BootstrapFormMixin(object):
    placeholders = {}

    def __init__(self, *args, **kwargs):
        super(BootstrapFormMixin, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            if self.fields[field].widget.attrs.get('class'):
                self.fields[field].widget.attrs['class'] += ' form-control'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control'

            if field in getattr(self, 'placeholders'):
                placeholder = self.placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
