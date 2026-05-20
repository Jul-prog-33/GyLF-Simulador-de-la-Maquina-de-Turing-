from django import forms


class MachineUploadForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=120, required=False)
    description = forms.CharField(label="Descripción", widget=forms.Textarea(attrs={"rows": 3}), required=False)
    file = forms.FileField(label="Archivo .mt")

    def clean_file(self):
        file = self.cleaned_data["file"]
        if not file.name.endswith(".mt"):
            raise forms.ValidationError("El archivo debe tener extensión .mt")
        return file


class SimulationForm(forms.Form):
    input_string = forms.CharField(label="Cadena de entrada", max_length=500, required=False)
    max_steps = forms.IntegerField(label="Límite de pasos", min_value=1, max_value=100000, initial=100)
