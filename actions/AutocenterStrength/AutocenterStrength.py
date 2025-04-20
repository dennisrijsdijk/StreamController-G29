from GtkHelper.GenerativeUI.ScaleRow import ScaleRow
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.PluginManager.EventAssigner import EventAssigner

class AutocenterStrength(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = True

        self.value_slider = ScaleRow(
            action_core=self,
            var_name="value",
            default_value=0,
            min=0,
            max=100,
            title="Autocenter Strength",
            step=1,
            digits=0,
            draw_value=True,
            round_digits=True,
            add_text_entry=True,
            text_entry_max_length=3,
            can_reset=False
        )

        self.event_manager.add_event_assigner(
            EventAssigner(
                id="set-auto-center",
                ui_label="Set Auto-Center Value",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_key_down
            )
        )

    def get_config_rows(self):
        return [
            self.value_slider.widget
        ]

    def _on_key_down(self, _):
        self.plugin_base.backend.set_autocenter_strength(self.value_slider.get_value())

    def on_tick(self):
        self.set_top_label("SET")
        self.set_center_label("CENTER")
        self.set_bottom_label(str(round(self.value_slider.get_value(), 0)) + "%")