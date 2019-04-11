import os

from .forms import ChangeEnvVariableForm

def create_changeenvvarform(button_name, label, forms_list, post_data=None):
    form = ChangeEnvVariableForm(post_data)
    form.button_name = button_name
    form.fields['new_value'].label = label
    forms_list.append(form)
    return form, forms_list


def save_changeenvvarform(form, button_name, label, forms_list):
    os.environ[label] = str(form.cleaned_data['new_value'])
    forms_list.remove(form)
    info2 = (True, label)
    form, forms_list = create_changeenvvarform(button_name, label, forms_list)

    return form, forms_list, info2
