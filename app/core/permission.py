from starlette import status
from starlette.requests import Request
from fastapi import HTTPException


class AbstractPermission(object):
    error_msg = "Access Forbidden"

    status_code = status.HTTP_403_FORBIDDEN

    def __init__(self, request: Request):
        self.request = request
        self.session = request.app.general_session

    async def has_permissions(self) -> bool:
        raise NotImplementedError

    async def check_permission(self):
        checked = await self.has_permissions()
        return checked


class PermissionsDependency(object):
    def __init__(self, permissions_classes: list):
        self.permissions_classes = permissions_classes

    async def __call__(self, request: Request):
        """
        Add gather in the future
        :param request: request from client
        :return:
        """

        for permission_class in self.permissions_classes:
            checked = await permission_class(request=request).check_permission()
            if not checked:
                raise HTTPException(
                    status_code=permission_class.status_code,
                    detail={"detail": permission_class.error_msg},
                )


class OrPermissionsDependency(PermissionsDependency):
    error_msg = "Access Forbidden"

    status_code = status.HTTP_403_FORBIDDEN

    async def __call__(self, request: Request):
        """
        Add gather in the future
        :param request: request from client
        :return:
        """
        checked = False
        for permission_class in self.permissions_classes:
            checked = await permission_class(request=request).check_permission()
            if checked:
                break

        if not checked:
            raise HTTPException(
                status_code=self.status_code, detail={"detail": self.error_msg}
            )
