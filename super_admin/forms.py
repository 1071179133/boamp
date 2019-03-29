from django.forms import forms,ModelForm
from databases_models import models

def create_model_form(request,admin_class):
    """type动态生成model form"""

    def __new__(cls,*args,**kwargs):
        '''使用new方法给model_form生成的表单添加 Bootstrap  form-control样式'''
        #print("base fields:",cls.base_fields)
        for field_name,field_obj in cls.base_fields.items():
            field_obj.widget.attrs['class'] = 'form-control'
        return ModelForm.__new__(cls)

    class Meta:
        model = admin_class.model
        fields = "__all__"
    attrs = {"Meta":Meta}
    _model_form_class = type("DynamicModelForm",(ModelForm,),attrs) #动态生成ModelForm
    #setattr(_model_form_class,'Meta',Meta) #相当于attrs = {"Meta":Meta},把类当作参数动态生成ModelForm
    #print("_model_form_class:",_model_form_class.Meta.model)
    setattr(_model_form_class,'__new__',__new__)

    return _model_form_class