class DBConnectionErr(Exception):
    """
    Когда возникли проблемы с подключение к базе данных
    """
    pass


class ScreenManagerException(Exception):
    """
    Когда пытаешься удалить объект экрана, когда его еще нет
    """
    pass