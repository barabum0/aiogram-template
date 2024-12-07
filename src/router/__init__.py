from aiogram import Router

from src.router.main import router as main_router

router = Router()
router.include_routers(main_router)
