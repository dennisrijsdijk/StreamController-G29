from GtkHelper.GenerativeUI.ComboRow import ComboRow
from GtkHelper.ComboRow import SimpleComboRowItem
from src.backend.PluginManager.ActionCore import ActionCore

stats = [ "range", "autocenter" ]
stats_labels = [ "Range", "Auto Center" ]
stats_options = [SimpleComboRowItem(x, y) for x, y in zip(stats, stats_labels)]
positions = [ "top", "center", "bottom" ]
positions_labels = [ "Top", "Middle", "Bottom" ]
positions_options = [SimpleComboRowItem(x, y) for x, y in zip(positions, positions_labels)]

class DisplayStat(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = True

        self.stat_row = ComboRow(
            action_core=self,
            var_name="stat",
            default_value=stats_options[0],
            items=stats_options,
            title="Stat",
            complex_var_name=False
        )

        self.stat_position_row = ComboRow(
            action_core=self,
            var_name="stat_pos",
            default_value=positions_options[1],
            items=positions_options,
            title="Stat Position",
            complex_var_name=False
        )

        self.stat_label_pos_row = ComboRow(
            action_core=self,
            var_name="stat_label_pos",
            default_value=positions_options[0],
            items=positions_options,
            title="Label Position",
            complex_var_name=False
        )

    def get_config_rows(self):
        return [
            self.stat_row.widget,
            self.stat_position_row.widget,
            self.stat_label_pos_row.widget
        ]

    def on_tick(self):
        stat_val = self.stat_row.get_value("range")
        pos = self.stat_position_row.get_value("center")
        label_pos = self.stat_label_pos_row.get_value("top")

        stat = ""
        match stat_val:
            case "range":
                stat = f"{self.plugin_base.backend.get_rotation_range()}°"
            case "autocenter":
                stat = f"{self.plugin_base.backend.get_autocenter_strength()}%"
            case _:
                return
        label = stats_labels[stats.index(stat_val)]

        self.set_label(stat, pos)
        self.set_label(label, label_pos)