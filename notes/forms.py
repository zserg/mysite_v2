from django import forms

class NoteForm(forms.Form):
    note_text = forms.CharField(widget=forms.Textarea)

class DeleteNoteForm(forms.Form):
   i = 0




