import collections
import pytz
from datetime import datetime
from marshmallow import ValidationError, Schema, fields, utils
from marshmallow_sqlalchemy import ModelSchemaOpts, ModelSchema, ModelConverter


NOT_EMPTY_REGEX = r'^(?!\s*$).+'


class USchema(Schema):
    def all_or_none_of(self, data, *keys):
        if all(key in data for key in keys):
            return
        if all(key not in data for key in keys):
            return
        raise ValidationError(
            'All of {} must be existed or not in the same time'.format(keys)
        )

    def exactly_one_of(self, data, *keys):
        if sum(key in data for key in keys) != 1:
            raise ValidationError(
                'Only one of {} must be provided'.format(keys))

    def nothing_or_one_of(self, data, *keys):
        sum_key = sum(key in data for key in keys)
        if sum_key not in [0, 1]:
            raise ValidationError(
                'Nothing or one of {} must be provided'.format(keys))

    def at_least_one_of(self, data, *keys):
        if any(key in data for key in keys):
            return
        raise ValidationError(
            'At least one of {} must be existed'.format(keys)
        )

    def cast_num_to_str(self, data, *keys):
        for key in keys:
            if key in data and isinstance(data[key], (int, float)):
                data[key] = str(data[key])
        return data

    def check_duplicate(self, items, type='Resource'):
        list_resource_duplicate = (
            [item for item, count
             in collections.Counter(items).items()
             if count > 1])

        if len(list_resource_duplicate) > 0:
            list_resource_duplicate = [str(resource)
                                       for resource in list_resource_duplicate]
            raise ValidationError('{} is duplicate: {}'.format(
                type,
                ' '.join(list_resource_duplicate)
            ))

    def check_datetime(self, data):
        try:
            min_created_at = data.get('min_created_at')
            max_created_at = data.get('max_created_at')
            min_rf_created_at = data.get('min_rf_created_at')
            max_rf_created_at = data.get('max_rf_created_at')
            min_ff_created_at = data.get('min_ff_created_at')
            max_ff_created_at = data.get('max_ff_created_at')
            if min_created_at:
                data['min_created_at'] = datetime.fromisoformat(
                    min_created_at
                ).astimezone(pytz.utc)
            if max_created_at:
                data['max_created_at'] = datetime.fromisoformat(
                    max_created_at
                ).astimezone(pytz.utc)
            if min_rf_created_at:
                data['min_rf_created_at'] = datetime.fromisoformat(
                    min_rf_created_at
                ).astimezone(pytz.utc)
            if max_rf_created_at:
                data['max_rf_created_at'] = datetime.fromisoformat(
                    max_rf_created_at
                ).astimezone(pytz.utc)
            if min_ff_created_at:
                data['min_ff_created_at'] = datetime.fromisoformat(
                    min_ff_created_at
                ).astimezone(pytz.utc)
            if max_ff_created_at:
                data['max_ff_created_at'] = datetime.fromisoformat(
                    max_ff_created_at
                ).astimezone(pytz.utc)
        except Exception:
            raise ValidationError('Invalid format date')


class UParamList(fields.List):
    def _deserialize(self, value, attr, data, **kwargs):
        if not utils.is_collection(value):
            value = [value]
        return super(UParamList, self)._deserialize(
            value, attr, data, **kwargs)


class BaseModelConverter(ModelConverter):
    def property2field(self, prop, instance=True, field_class=None, **kwargs):
        if hasattr(prop, "direction"):
            return None
        return super(BaseModelConverter, self).property2field(
            prop, instance=True, field_class=None, **kwargs
        )


class BaseOpts(ModelSchemaOpts):
    def __init__(self, meta, ordered=True):
        meta.include_fk = True
        meta.model_converter = BaseModelConverter
        super(BaseOpts, self).__init__(meta)


class ModelBaseSchema(ModelSchema):
    OPTIONS_CLASS = BaseOpts
