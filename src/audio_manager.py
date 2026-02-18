"""
音频管理器模块

解决 Flet 0.80.5 中 Audio 控件必须先添加到 page 的问题
参考 FilePicker 和 PermissionHandler 的处理方式，将 Audio 控件添加到 page.overlay
这样可以确保音频控件在路由切换时不会被清除
"""

import flet as ft
import flet_audio as fta
import asyncio

class AudioManager:
    """音频管理器类，统一管理所有音频控件"""
    
    def __init__(self, page: ft.Page):
        """
        初始化音频管理器
        
        Args:
            page: Flet 页面对象
        """
        self.page = page
        
        # 创建所有音频控件
        self.bgm = fta.Audio(
            src="/audio/bgm/ambient_loop.wav",
            autoplay=False,
            volume=0.2,  # ✅ 调小音量：从 0.6 改为 0.3
            release_mode=fta.ReleaseMode.LOOP
        )
        
        self.se_welcome_confirm = fta.Audio(
            src="/audio/se/welcome_confirm.wav",
            autoplay=False,
            volume=1.0,
            release_mode=fta.ReleaseMode.STOP
        )
        
        self.se_wheel_tick = fta.Audio(
            src="/audio/se/wheel_tick.wav",
            autoplay=False,
            volume=1.0,
            release_mode=fta.ReleaseMode.STOP
        )
        
        self.se_card_focus = fta.Audio(
            src="/audio/se/card_focus.wav",
            autoplay=False,
            volume=0.9,
            release_mode=fta.ReleaseMode.STOP
        )
        
        self.se_topic_start = fta.Audio(
            src="/audio/se/topic_start.wav",
            autoplay=False,
            volume=1.0,
            release_mode=fta.ReleaseMode.STOP
        )
        
        self.se_splash = fta.Audio(
            src="/audio/se/splash_logo.wav",
            autoplay=False,
            release_mode=fta.ReleaseMode.STOP
        )
        
        # BGM 状态管理
        self.is_bgm_enabled = False  # 记录 BGM 是否处于"应该播放"状态
    
    def get_controls(self) -> list:
        """
        获取所有音频控件列表
        
        Returns:
            包含所有 Audio 实例的列表，用于注入到 View 的 controls 中
        """
        return [
            self.bgm,
            self.se_welcome_confirm,
            self.se_wheel_tick,
            self.se_card_focus,
            self.se_topic_start,
            self.se_splash
        ]
    
    async def play_bgm(self):
        """播放背景音乐"""
        try:
            self.is_bgm_enabled = True
            await self.bgm.play()
            print("背景音乐开始播放")
        except Exception as e:
            print(f"背景音乐播放失败: {e}")
    
    async def stop_bgm(self):
        """停止背景音乐"""
        try:
            self.is_bgm_enabled = False
            await self.bgm.pause()
        except Exception as e:
            print(f"背景音乐停止失败: {e}")
    
    async def play_welcome_confirm(self):
        """播放欢迎确认音效"""
        try:
            await self.se_welcome_confirm.play()
        except Exception as e:
            print(f"欢迎确认音效播放失败: {e}")
    
    async def play_wheel_tick(self):
        """播放滚轮滴答音效"""
        try:
            await self.se_wheel_tick.play()
        except Exception as e:
            # 滚动音效失败可以忽略
            pass
    
    async def play_card_focus(self):
        """播放卡片聚焦音效"""
        try:
            await self.se_card_focus.play()
        except Exception as e:
            print(f"卡片聚焦音效播放失败: {e}")
    
    async def play_topic_start(self):
        """播放话题开始音效"""
        try:
            await self.se_topic_start.play()
        except Exception as e:
            print(f"话题开始音效播放失败: {e}")
    
    async def play_splash(self):
        """播放开屏音效"""
        try:
            await self.se_splash.play()
        except Exception as e:
            print(f"开屏音效播放失败: {e}")
    
    async def pause_bgm(self):
        """暂停背景音乐（不改变启用状态）"""
        try:
            await self.bgm.pause()
            print("背景音乐已暂停（系统暂停）")
        except Exception as e:
            print(f"背景音乐暂停失败: {e}")
    
    async def resume_bgm(self):
        """恢复背景音乐（仅在启用状态下恢复）"""
        if self.is_bgm_enabled:
            try:
                await self.bgm.resume()
                print("背景音乐已恢复")
            except Exception as e:
                print(f"背景音乐恢复失败: {e}")
        else:
            print("背景音乐未启用，跳过恢复")
