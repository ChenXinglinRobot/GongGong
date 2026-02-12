"""
视图模块包
统一导出所有视图函数
"""

from .menu import get_menu_view
from .setup import get_setup_view
from .player import get_player_view

__all__ = [
    "get_menu_view",
    "get_setup_view", 
    "get_player_view"
]
