from tools.base import Tool, ToolExample
from msedge.selenium_tools import Edge, EdgeOptions

class EdgeTool(Tool):
    def __init__(self):
        super().__init__(
            name="EDGE",
            description="Helper to control the Microsoft Edge web browser.",
            examples=[
                ToolExample(
                    input="Open the Forge MDK files",
                    output="[EDGE(open https://files.minecraftforge.net/) -> 0]"
                ),
                ToolExample(
                    input="Find the latest MDK",
                    output="""[EDGE(js document.querySelector("a[title='Mdk']").href) -> 0]""",
                ),
            ],
            method=self.invoke
        )

    def invoke(self, params) -> str:
        print("hehe")
        # create EdgeOptions object and set preferences
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("disable-gpu")
        options.add_argument("disable-extensions")

        # create Edge WebDriver object
        driver = Edge(options=options)

        # execute the commands specified in params
        output = []
        for command in params.split("\n"):
            if command.startswith("open"):
                url = command.split(" ")[1]
                driver.get(url)
                output.append("[EDGE(open {0}) -> {1}]".format(url, 0))
            elif command.startswith("js"):
                script = command.split(" ", 1)[1]
                result = driver.execute_script(script)
                output.append("[EDGE(js {0}) -> {1}]".format(script, result))
            else:
                output.append("[ERROR: unrecognized command '{0}']".format(command))

        # close the browser
        driver.quit()

        return "\n".join(output)