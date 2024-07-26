def paginate(queryset, skip: int, limit: int):
    return queryset.offset(skip).limit(limit).all()
