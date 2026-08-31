class BaseService:

    def _update_instance_entity(self, data: dict, entity):
        for key, value in data.items():
            setattr(entity, key, value)
        return entity