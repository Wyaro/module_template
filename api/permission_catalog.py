from .permissions import MODULE_NAME, TEMPLATE_VIEW

PERMISSION_CATALOG = {
    'module_name': MODULE_NAME,
    'module_label': 'Шаблон модуля',
    'user_description': (
        'Учебный раздел с примерами типовых экранов ERGO MS: списки, формы и паттерны интерфейса. '
        'Данные учебные и не влияют на рабочие модули.'
    ),
    'permissions': {
        TEMPLATE_VIEW: 'Просмотр учебных элементов шаблона модуля',
    },
}
