from src.repositories.base_repository import BaseRepository


class ItemRepository(BaseRepository):
    def __init__(self):
        # super().__init__(collection)
        pass

    async def find_by_name(self, name: str):
        return await self.get_one_by_query({"name": name})
