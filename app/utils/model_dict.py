from datetime import datetime, date

def model_to_dict(model):

    if model is None:
        return None

    result = {}

    for column in model.__table__.columns:
        value = getattr(model, column.name)

        if isinstance(value, (datetime, date)):
            value = value.isoformat()

        result[column.name] = value

    return result
