import flet as ft
import asyncio
import time
from typing import List, Callable, Awaitable
from data_loader import Topic
from enum import Enum

class CardState(Enum):
    SELECTION = "selection"
    FOCUS = "focus"
    ENTER = "enter"

def get_welcome_view(page: ft.Page, topics: List[Topic], on_topic_enter: Callable[[Topic], Awaitable[None]]):
    
    # --- 1. 数据准备 ---
    first_cover = topics[0].cover_image_path if topics else ""
    
    # 状态变量
    current_scroll_index = 0.0 
    target_index = 0 
    current_state = CardState.SELECTION
    
    # 视觉参数
    ITEM_HEIGHT = 80 
    
    # --- 2. 核心组件定义 ---

    # [背景层]
    bg_image = ft.Image(
        src=first_cover,
        fit=ft.BoxFit.COVER,
        opacity=0.6,
    )
    
    # 动态模糊层
    bg_blur_weak = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK12, 
        blur=ft.Blur(5, 5, ft.BlurTileMode.CLAMP), 
    )

    bg_blur_strong = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK45, 
        blur=ft.Blur(30, 30, ft.BlurTileMode.CLAMP), 
        opacity=0, 
        animate_opacity=ft.Animation(1000, ft.AnimationCurve.EASE_OUT), 
    )

    bg_layer = ft.Stack(
        controls=[bg_image, bg_blur_weak, bg_blur_strong], 
        expand=True
    )

    # [前景欢迎卡片]
    welcome_card = ft.Container(
        width=480, height=270,
        alignment=ft.Alignment(0, 0),
        image=ft.DecorationImage(src=first_cover, fit=ft.BoxFit.COVER) if first_cover else None,
        border_radius=12,
        shadow=ft.BoxShadow(blur_radius=20, color=ft.Colors.BLACK),
        scale=1.0, opacity=1.0,
        animate_scale=ft.Animation(800, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
    )

    enter_btn = ft.Container(
        content=ft.Row(
            [ft.Text("点击进入回忆", size=20, color="white"), ft.Icon(ft.Icons.ARROW_FORWARD, color="white")],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        padding=ft.padding.symmetric(horizontal=30, vertical=15),
        border_radius=30,
        bgcolor=ft.Colors.WHITE24,
        animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
        on_click=lambda e: asyncio.create_task(run_transition(e)),
    )

    welcome_layer = ft.Column(
        [welcome_card, ft.Container(height=40), enter_btn],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    welcome_container = ft.Container(
        content=welcome_layer,
        alignment=ft.Alignment(0,0),
        expand=True
    )

    # --- 3. 拨盘与选择层 ---
    
    # 解除剪裁
    cards_stack = ft.Stack(
        expand=True,
        clip_behavior=ft.ClipBehavior.NONE 
    )
    
    right_image_switcher = ft.AnimatedSwitcher(
        content=ft.Container(key="init"),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=500,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
    )

    right_panel = ft.Container(
        content=right_image_switcher,
        expand=True,
        padding=ft.padding.only(left=320, right=50, top=50, bottom=50),
        opacity=0, scale=0.9,
        # 这里的动画曲线决定了回弹的质感，EASE_OUT_CUBIC 很有弹性
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(800, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    # 解除左侧面板剪裁
    left_panel = ft.Container(
        content=cards_stack,
        width=300,
        offset=ft.Offset(-1.2, 0),
        opacity=0,
        clip_behavior=ft.ClipBehavior.NONE, 
        animate_offset=ft.Animation(800, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_opacity=ft.Animation(800, ft.AnimationCurve.EASE_OUT),
    )

    selection_layer = ft.Stack(
        controls=[right_panel, left_panel], 
        expand=True,
        visible=False,
        clip_behavior=ft.ClipBehavior.NONE 
    )

    # --- 4. 逻辑处理 ---

    def get_topic_by_index(idx):
        if not topics: return None
        real_index = idx % len(topics)
        return topics[real_index]

    def render_cards(is_dragging=False):
        cards_stack.controls.clear()
        
        center_y = 300 
        base_idx = round(current_scroll_index)
        
        for i in range(base_idx - 3, base_idx + 4):
            topic = get_topic_by_index(i)
            if not topic: continue

            rel_pos = i - current_scroll_index 
            is_center_highlight = (abs(rel_pos) < 0.1)
            
            offset_x = -1 * (abs(rel_pos) ** 2) * 15
            top_y = center_y + (rel_pos * ITEM_HEIGHT) - 30
            
            scale = 1.1 - (abs(rel_pos) * 0.1) 
            opacity = max(0, 1.0 - (abs(rel_pos) * 0.3)) 
            
            if is_center_highlight and current_state == CardState.FOCUS:
                offset_x += 60 
                scale = 1.3
                opacity = 1.0

            anim_duration = 0 if is_dragging else 300
            
            card_key = f"card_{i}_{topic.id}"

            card = ft.Container(
                key=card_key,
                content=ft.Text(topic.name, size=20 if is_center_highlight else 16, weight="bold", no_wrap=True),
                width=240, height=60, 
                bgcolor=ft.Colors.WHITE24 if is_center_highlight else ft.Colors.WHITE10,
                blur=ft.Blur(5, 5), 
                border_radius=10,
                padding=ft.padding.only(left=20),
                alignment=ft.Alignment.CENTER_LEFT,
                left=50 + offset_x,
                top=top_y,
                opacity=opacity,
                scale=scale,
                animate_position=ft.Animation(anim_duration, ft.AnimationCurve.EASE_OUT),
                animate_scale=ft.Animation(anim_duration, ft.AnimationCurve.EASE_OUT),
                animate_opacity=ft.Animation(anim_duration, ft.AnimationCurve.EASE_OUT),
                on_click=lambda e, virtual_idx=i: asyncio.create_task(handle_click(virtual_idx))
            )
            cards_stack.controls.append(card)
        
        cards_stack.update()

    def update_right_image():
        current_real_topic = get_topic_by_index(round(current_scroll_index))
        if not current_real_topic: return
        
        img_src = current_real_topic.cover_image_path
        
        if right_image_switcher.content.key == f"img_{current_real_topic.id}":
            return

        right_image_switcher.content = ft.Container(
            key=f"img_{current_real_topic.id}",
            image=ft.DecorationImage(src=img_src, fit=ft.BoxFit.COVER),
            border_radius=16,
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK45), 
        )
        right_image_switcher.update()

    async def handle_click(virtual_index):
        nonlocal current_scroll_index, target_index, current_state
        
        # 1. 点击切换
        if virtual_index != round(current_scroll_index):
            current_state = CardState.SELECTION
            target_index = virtual_index
            current_scroll_index = float(target_index)
            
            right_panel.scale = 1.0
            right_panel.update()
            
            render_cards(is_dragging=False)
            update_right_image()
            return

        # 2. 状态流转
        if current_state == CardState.SELECTION:
            current_state = CardState.FOCUS
            render_cards() 
            right_panel.scale = 1.2 # 放大
            right_panel.update()
        elif current_state == CardState.FOCUS:
            current_state = CardState.ENTER
            real_topic = get_topic_by_index(round(current_scroll_index))
            await on_topic_enter(real_topic)

    # --- 5. 手势与惯性逻辑 ---
    
    def on_pan_update(e: ft.DragUpdateEvent):
        nonlocal current_scroll_index, current_state
        
        if current_state == CardState.FOCUS:
            current_state = CardState.SELECTION
        
        # 🔥【新增效果】：只要拨动，就缩小一点点
        # 无论之前是在Focus(1.2)还是Selection(1.0)，都统一缩到 0.95
        # 这种“受力收缩”的感觉会非常解压
        right_panel.scale = 0.95 
        right_panel.update()

        delta_index = -e.local_delta.y / ITEM_HEIGHT 
        
        current_scroll_index += delta_index
        render_cards(is_dragging=True)

    def on_pan_end(e: ft.DragEndEvent):
        nonlocal current_scroll_index, target_index
        
        target_index = round(current_scroll_index)
        current_scroll_index = float(target_index)
        
        # 🔥【新增效果】：松手回弹
        # 恢复到默认大小 1.0
        right_panel.scale = 1.0
        right_panel.update()
        
        render_cards(is_dragging=False) 
        update_right_image()

    left_panel_gesture = ft.GestureDetector(
        content=left_panel,
        on_vertical_drag_update=on_pan_update,
        on_vertical_drag_end=on_pan_end,
    )
    
    # --- 6. 转场动画 ---
    
    async def run_transition(e):
        enter_btn.opacity = 0
        welcome_card.scale = 3.0
        welcome_card.opacity = 0
        
        bg_blur_strong.opacity = 1
        bg_blur_strong.update()
        
        page.update()

        await asyncio.sleep(0.6)

        welcome_container.visible = False
        selection_layer.visible = True
        
        render_cards()
        update_right_image()
        page.update()

        await asyncio.sleep(0.05)
        left_panel.offset = ft.Offset(0, 0)
        left_panel.opacity = 1
        right_panel.opacity = 1
        right_panel.scale = 1.0
        page.update()

    # --- 7. 组装 ---
    
    selection_layer.controls[1] = left_panel_gesture 
    
    root = ft.Stack(
        controls=[bg_layer, welcome_container, selection_layer],
        expand=True,
    )

    return ft.View(
        route="/",
        controls=[root],
        padding=0,
        bgcolor=ft.Colors.BLACK,
    )