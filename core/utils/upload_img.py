from core.utils.get_meta_name import get_model_name

def upload_img(instance, filename):
    modelName = get_model_name(instance)
    if(instance):
        return f"{modelName}/{instance.id}/{filename}"
    else:
        return f"{modelName}/{filename}"