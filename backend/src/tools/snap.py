from tools.base import Tool, ToolExample
from typing import *

class SnapTool(Tool):
    def __init__(self):
        super().__init__(
            name="SNAP",
            description="Rearranges windows on the screen. Takes the name of the window and the position as arguments.",
            examples=[
                ToolExample(
                    input="Please move chrome to the left.",
                    output="Sure thing! [SNAP(Chrome, left) -> Chrome not found] Oh. I couldn't find that program."
                ),
                ToolExample(
                    input="Please move chrome to the left.",
                    output="Sure thing! [SNAP(Chrome, left) -> None] Chrome should now be on the left."
                ),
                ToolExample(
                    input="Can you move notepad to my second monitor.",
                    output="Sure thing! [SNAP(Notepad, second monitor) -> None] Notepad should now be on your second monitor."
                ),
                ToolExample(
                    input="Arrange Discord and Spotify on my right monitor.",
                    output="Sure thing! [SNAP(Discord, right monitor right side) -> None] [SNAP(Spotify, right monitor right side)] Discord and Spotify should now be side-by-side on your monitor."
                ),
                ToolExample(
                    input="Move OBS to the top right corner.",
                    output="Sure thing! [SNAP(OBS, top right) -> None] OBS should now be in the top right corner."
                ),
            ],
            method=self.invoke
        )

    def invoke(self, params: str) -> str:
        window, position = params.split(",")

        import ctypes
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        found = self.get_process_by_natural_name(window)
        if found is None:
            return f"{window} not found"
        handle, title, exe = found
        if handle == 0:
            return f"{window} not found"
        pos = self.pos2pos(position)
        user32.MoveWindow(handle, *pos, True)
        # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-showwindow
        user32.ShowWindow(handle, 8)
        user32.SetForegroundWindow(handle)
        return f"{exe} to {pos}"

    def list_windows(self) -> List[Tuple[int, str, str]]:
        import psutil, win32process, win32gui
        def get_process_name(handle):
            pid = win32process.GetWindowThreadProcessId(handle) #This produces a list of PIDs active window relates to
            return (psutil.Process(pid[-1]).name()) #pid[-1] is the most likely to survive last longer
        rtn = []
        def winEnumHandler(hwnd: int, ctx ):
            nonlocal rtn
            if win32gui.IsWindowVisible( hwnd ):
                rtn.append((hwnd, win32gui.GetWindowText( hwnd ), get_process_name(hwnd)))
        win32gui.EnumWindows( winEnumHandler, None )
        return rtn

    def get_process_by_natural_name(self, name: str) -> None | Tuple[int, str, str]:
        from fuzzywuzzy import fuzz
        ranked = [(max([fuzz.ratio(str(feature), name) for feature in x]),x) for x in self.list_windows()]
        ranked = sorted(ranked, key=lambda x: x[0], reverse=True)
        ranked = [x for x in ranked if x[0] > 50]
        return None if len(ranked) == 0 else ranked[0][1]

    def pos2pos(self, pos: str) -> Tuple[int,int,int,int]:
        from screeninfo import get_monitors
        monitors = get_monitors()
        left = sorted(monitors, key=lambda x: x.x)[0]
        right = sorted(monitors, key=lambda x: x.x, reverse=True)[0]
        main = [x for x in monitors if x.is_primary][0]
        corners = {
            "top left": lambda m: (m.x, m.y, m.width//2, m.height//2),
            "top right": lambda m: (m.x + m.width//2, m.y, m.width//2, m.height//2),
            "bottom left": lambda m: (m.x, m.y + m.height//2, m.width//2, m.height//2),
            "bottom right": lambda m: (m.x + m.width//2, m.y + m.height//2, m.width//2, m.height//2),
        }
        lookup = {}
        for corner, func in corners.items():
            lookup[f"left monitor, {corner}"] = func(left)
            lookup[f"third monitor, {corner}"] = func(left)
            
            lookup[f"main monitor, {corner}"] = func(main)

            lookup[f"right monitor, {corner}"] = func(right)
            lookup[f"second monitor, {corner}"] = func(right)
            lookup[f"secondary monitor, {corner}"] = func(right)
        
        lookup[f"main monitor, full"] = (main.x, main.y, main.width, main.height)
        
        lookup[f"left monitor, full"] = (left.x, left.y, left.width, left.height)
        lookup[f"third monitor, full"] = (left.x, left.y, left.width, left.height)
        
        lookup[f"right monitor, full"] = (right.x, right.y, right.width, right.height)
        lookup[f"secondary monitor, full"] = (right.x, right.y, right.width, right.height)

        from fuzzywuzzy import fuzz
        x = sorted([(fuzz.ratio(label, pos),data) for label,data in lookup.items()], key=lambda x: x[0], reverse=True)
        # print(x)
        return x[0][1]
