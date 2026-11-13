from asgiref.sync import iscoroutinefunction, markcoroutinefunction
class TenantMiddleware:
    sync_capable = True
    async_capable = True
    def __init__(self, get_response):
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)
    def _tag(self, request):
        request.tenant_id = request.headers.get("X-Tenant-ID", "demo")
    def __call__(self, request):
        if iscoroutinefunction(self):
            return self.__acall__(request)
        self._tag(request)
        return self.get_response(request)
    async def __acall__(self, request):
        self._tag(request)
        return await self.get_response(request)