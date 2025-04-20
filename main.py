import os.path

from src.backend.PluginManager.PluginBase import PluginBase
from src.backend.PluginManager.ActionHolder import ActionHolder

# Import actions
from .actions.AutocenterStrength.AutocenterStrength import AutocenterStrength
from .actions.DisplayStat.DisplayStat import DisplayStat
from .actions.RotationRange.RotationRange import RotationRange

class PluginTemplate(PluginBase):
    def __init__(self):
        super().__init__()
        self.launch_backend(os.path.join(self.PATH, "backend", "backend.py"), os.path.join(self.PATH, "backend", ".venv"))
        self.wait_for_backend(5)

        self.autocenter_action_holder = ActionHolder(
            plugin_base = self,
            action_base = AutocenterStrength,
            action_id = "gg_dennis_g29::AutocenterStrength",
            action_name = "Set Auto-Center Strength",
        )

        self.display_action_holder = ActionHolder(
            plugin_base=self,
            action_base=DisplayStat,
            action_id="gg_dennis_g29::DisplayStat",
            action_name="Display Stat",
        )

        self.rotation_action_holder = ActionHolder(
            plugin_base=self,
            action_base=RotationRange,
            action_id="gg_dennis_g29::RotationRange",
            action_name="Set Rotation Range",
        )

        self.add_action_holder(self.autocenter_action_holder)
        self.add_action_holder(self.display_action_holder)
        self.add_action_holder(self.rotation_action_holder)

        # Register plugin
        self.register(
            plugin_name = "Logitech G29 Control",
            github_repo = "https://github.com/dennisrijsdijk/StreamController-G29",
            plugin_version = "0.0.1",
            app_version = "1.1.1-alpha"
        )