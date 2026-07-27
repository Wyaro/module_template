from src.core.cms.adp.base_permissions import BaseModulePermission

MODULE_NAME = 'module_template'

TEMPLATE_VIEW = 'module_template_view'


class _BaseModuleTemplatePermission(BaseModulePermission):
    module_name = MODULE_NAME


class CanViewModuleTemplate(_BaseModuleTemplatePermission):
    required_permission = TEMPLATE_VIEW
