from tools.base import Tool, ToolExample

class ForgeMDKTool(Tool):
    def __init__(self):
        super().__init__(
            name="FORGE_MDK",
            description="Minecraft Forge MDK helper",
            examples=[
                ToolExample(
                    input="What's the latest Forge MDK?",
                    output="The latest Minecraft Forge MDK is for [MDK(latest) -> 1.19.3 - 44.1.23 from 3 days ago] 1.19.3 - 44.1.23 from 3 days ago."
                ),
                ToolExample(
                    input="Download the latest Forge MDK to C:\\temp\\forge",
                    output="The latest Minecraft Forge MDK is available at [MDK(latest-url) -> https://adfoc.us/serve/sitelinks/?id=271228&url=https://maven.minecraftforge.net/net/minecraftforge/forge/1.19.3-44.1.23/forge-1.19.3-44.1.23-mdk.zip], so we can download it from there [DOWNLOAD($rtn) -> took 3s], which took three seconds."
                ),
            ],
            method=self.invoke
        )
    def invoke(self, paramstring: str) -> str:
        print(f"received {paramstring}")