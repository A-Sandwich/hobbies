class ViewUtility:
    @staticmethod
    def get_direction(direction, default='desc'):
        direction = default if not direction else direction
        # '-' is specific to django query order
        return '-' if direction.lower() == 'desc' else ''
