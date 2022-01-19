import collections


def iterable_to_dict(iterable_or_model, field='id'):
    if not isinstance(iterable_or_model, collections.abc.Iterable):
        iterable_or_model = iterable_or_model.objects.all()

    return {getattr(e, field): e for e in iterable_or_model}
