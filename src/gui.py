"""Main GUI for the NHL Trade Analyzer application."""

import threading
import customtkinter as ctk
from tkinter import messagebox

from src.nhl_data import (
    get_team_names,
    get_team_color,
    POSITIONS,
    DRAFT_PICKS,
    SALARY_RETENTION_OPTIONS,
)
from src.analyzer import analyze_trade, format_analysis_text


# Theme constants
BG_DARK = "#0f0f1a"
BG_CARD = "#1a1a2e"
BG_INPUT = "#16213e"
ACCENT_BLUE = "#0f3460"
ACCENT_HIGHLIGHT = "#e94560"
TEXT_PRIMARY = "#ffffff"
TEXT_SECONDARY = "#a0a0b8"
BORDER_COLOR = "#2a2a4a"
SUCCESS_GREEN = "#00d26a"
WARNING_YELLOW = "#ffc107"
GRADE_COLORS = {
    "A+": "#00d26a", "A": "#00d26a", "A-": "#4caf50",
    "B+": "#8bc34a", "B": "#cddc39", "B-": "#ffeb3b",
    "C+": "#ffc107", "C": "#ff9800", "C-": "#ff5722",
    "D+": "#f44336", "D": "#e91e63", "D-": "#9c27b0",
    "F": "#6a0dad",
}


class TradeAssetFrame(ctk.CTkFrame):
    """Frame for adding and displaying trade assets for one team."""

    def __init__(self, master, team_name, team_color, **kwargs):
        super().__init__(master, fg_color=BG_CARD, corner_radius=12, **kwargs)
        self.team_name = team_name
        self.team_color = team_color
        self.assets = []

        self._build_ui()

    def _build_ui(self):
        # Team header
        self.header = ctk.CTkLabel(
            self,
            text=self.team_name,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.team_color,
        )
        self.header.pack(pady=(12, 4), padx=12)

        self.sub_header = ctk.CTkLabel(
            self,
            text="SENDS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        self.sub_header.pack(pady=(0, 8))

        # Asset type selector
        type_frame = ctk.CTkFrame(self, fg_color="transparent")
        type_frame.pack(fill="x", padx=12, pady=(0, 4))

        self.asset_type = ctk.CTkSegmentedButton(
            type_frame,
            values=["Player", "Pick", "Prospect"],
            font=ctk.CTkFont(size=12),
            fg_color=BG_INPUT,
            selected_color=ACCENT_HIGHLIGHT,
            selected_hover_color="#c93050",
            unselected_color=ACCENT_BLUE,
            unselected_hover_color="#1a4a7a",
            command=self._on_type_change,
        )
        self.asset_type.set("Player")
        self.asset_type.pack(fill="x")

        # Dynamic input area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=12, pady=4)

        self._build_player_inputs()

        # Add button
        self.add_btn = ctk.CTkButton(
            self,
            text="+ Add Asset",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT_HIGHLIGHT,
            hover_color="#c93050",
            height=34,
            corner_radius=8,
            command=self._add_asset,
        )
        self.add_btn.pack(fill="x", padx=12, pady=(4, 8))

        # Asset list
        self.list_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_INPUT,
            corner_radius=8,
            height=150,
        )
        self.list_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self.empty_label = ctk.CTkLabel(
            self.list_frame,
            text="No assets added yet",
            text_color=TEXT_SECONDARY,
            font=ctk.CTkFont(size=12, slant="italic"),
        )
        self.empty_label.pack(pady=20)

    def _clear_inputs(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

    def _build_player_inputs(self):
        self._clear_inputs()

        # Name
        self.name_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Player Name",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13),
            height=32,
        )
        self.name_entry.pack(fill="x", pady=2)

        row1 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        row1.pack(fill="x", pady=2)

        self.position_var = ctk.CTkComboBox(
            row1,
            values=POSITIONS,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=12),
            width=80,
            height=32,
        )
        self.position_var.set("C")
        self.position_var.pack(side="left", padx=(0, 4))

        self.age_entry = ctk.CTkEntry(
            row1,
            placeholder_text="Age",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12),
            width=60,
            height=32,
        )
        self.age_entry.pack(side="left", padx=4)

        self.cap_entry = ctk.CTkEntry(
            row1,
            placeholder_text="Cap Hit (e.g. 8.5M)",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12),
            height=32,
        )
        self.cap_entry.pack(side="left", fill="x", expand=True, padx=4)

        row2 = ctk.CTkFrame(self.input_frame, fg_color="transparent")
        row2.pack(fill="x", pady=2)

        self.years_entry = ctk.CTkEntry(
            row2,
            placeholder_text="Years Left",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=12),
            width=90,
            height=32,
        )
        self.years_entry.pack(side="left", padx=(0, 4))

        self.retention_var = ctk.CTkComboBox(
            row2,
            values=SALARY_RETENTION_OPTIONS,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=12),
            width=100,
            height=32,
        )
        self.retention_var.set("0%")
        self.retention_var.pack(side="left", padx=4)

        ctk.CTkLabel(
            row2, text="Retention", text_color=TEXT_SECONDARY, font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=(2, 0))

    def _build_pick_inputs(self):
        self._clear_inputs()

        self.pick_var = ctk.CTkComboBox(
            self.input_frame,
            values=DRAFT_PICKS,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=13),
            height=32,
        )
        self.pick_var.set(DRAFT_PICKS[0])
        self.pick_var.pack(fill="x", pady=2)

    def _build_prospect_inputs(self):
        self._clear_inputs()

        self.name_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Prospect Name",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13),
            height=32,
        )
        self.name_entry.pack(fill="x", pady=2)

        self.position_var = ctk.CTkComboBox(
            self.input_frame,
            values=POSITIONS,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=12),
            width=80,
            height=32,
        )
        self.position_var.set("C")
        self.position_var.pack(fill="x", pady=2)

    def _on_type_change(self, value):
        if value == "Player":
            self._build_player_inputs()
        elif value == "Pick":
            self._build_pick_inputs()
        elif value == "Prospect":
            self._build_prospect_inputs()

    def _add_asset(self):
        asset_type = self.asset_type.get()

        if asset_type == "Player":
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Missing Info", "Please enter a player name.")
                return
            asset = {
                "type": "player",
                "name": name,
                "position": self.position_var.get(),
                "age": self.age_entry.get().strip(),
                "cap_hit": self.cap_entry.get().strip(),
                "contract_years": self.years_entry.get().strip(),
                "retention": self.retention_var.get() if self.retention_var.get() != "0%" else "",
            }
            display = f"{name} ({asset['position']})"
            if asset["cap_hit"]:
                display += f" - ${asset['cap_hit']}"

        elif asset_type == "Pick":
            pick = self.pick_var.get()
            asset = {"type": "pick", "name": pick}
            display = f"📋 {pick}"

        elif asset_type == "Prospect":
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("Missing Info", "Please enter a prospect name.")
                return
            asset = {
                "type": "prospect",
                "name": name,
                "position": self.position_var.get(),
            }
            display = f"⭐ {name} ({asset['position']})"

        self.assets.append(asset)
        self._refresh_list()

        # Clear inputs
        if asset_type in ("Player", "Prospect"):
            self.name_entry.delete(0, "end")
            if asset_type == "Player":
                self.age_entry.delete(0, "end")
                self.cap_entry.delete(0, "end")
                self.years_entry.delete(0, "end")

    def _refresh_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        if not self.assets:
            self.empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No assets added yet",
                text_color=TEXT_SECONDARY,
                font=ctk.CTkFont(size=12, slant="italic"),
            )
            self.empty_label.pack(pady=20)
            return

        for i, asset in enumerate(self.assets):
            row = ctk.CTkFrame(self.list_frame, fg_color=BG_CARD, corner_radius=6, height=32)
            row.pack(fill="x", pady=2, padx=2)
            row.pack_propagate(False)

            if asset["type"] == "player":
                text = f"{asset['name']} ({asset.get('position', '')})"
                if asset.get("cap_hit"):
                    text += f"  ${asset['cap_hit']}"
                if asset.get("retention"):
                    text += f"  [{asset['retention']} ret.]"
            elif asset["type"] == "pick":
                text = f"Pick: {asset['name']}"
            else:
                text = f"Prospect: {asset['name']} ({asset.get('position', '')})"

            ctk.CTkLabel(
                row,
                text=text,
                font=ctk.CTkFont(size=12),
                text_color=TEXT_PRIMARY,
                anchor="w",
            ).pack(side="left", padx=8, fill="x", expand=True)

            remove_btn = ctk.CTkButton(
                row,
                text="✕",
                width=28,
                height=24,
                font=ctk.CTkFont(size=12),
                fg_color="#8B0000",
                hover_color="#B22222",
                corner_radius=4,
                command=lambda idx=i: self._remove_asset(idx),
            )
            remove_btn.pack(side="right", padx=4, pady=4)

    def _remove_asset(self, index):
        if 0 <= index < len(self.assets):
            self.assets.pop(index)
            self._refresh_list()

    def update_team(self, team_name, team_color):
        self.team_name = team_name
        self.team_color = team_color
        self.header.configure(text=team_name, text_color=team_color)

    def get_assets(self):
        return self.assets

    def clear_assets(self):
        self.assets.clear()
        self._refresh_list()


class SettingsWindow(ctk.CTkToplevel):
    """Settings window for API key and model configuration."""

    def __init__(self, master, current_key="", current_model="gpt-4o"):
        super().__init__(master)
        self.title("Settings")
        self.geometry("460x280")
        self.resizable(False, False)
        self.configure(fg_color=BG_DARK)

        self.api_key = current_key
        self.model = current_model
        self.saved = False

        self._build_ui()
        self.grab_set()

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=(16, 12))

        # API Key
        key_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=8)
        key_frame.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(
            key_frame,
            text="OpenAI API Key",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w", padx=12, pady=(8, 2))

        self.key_entry = ctk.CTkEntry(
            key_frame,
            placeholder_text="sk-...",
            show="*",
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            font=ctk.CTkFont(size=13),
            height=36,
        )
        self.key_entry.pack(fill="x", padx=12, pady=(0, 10))
        if self.api_key:
            self.key_entry.insert(0, self.api_key)

        # Model selection
        model_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=8)
        model_frame.pack(fill="x", padx=20, pady=4)

        ctk.CTkLabel(
            model_frame,
            text="AI Model",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w", padx=12, pady=(8, 2))

        self.model_combo = ctk.CTkComboBox(
            model_frame,
            values=["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=13),
            height=36,
        )
        self.model_combo.set(self.model)
        self.model_combo.pack(fill="x", padx=12, pady=(0, 10))

        # Save button
        ctk.CTkButton(
            self,
            text="Save Settings",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=SUCCESS_GREEN,
            hover_color="#00b359",
            text_color="#000000",
            height=38,
            corner_radius=8,
            command=self._save,
        ).pack(fill="x", padx=20, pady=(12, 16))

    def _save(self):
        self.api_key = self.key_entry.get().strip()
        self.model = self.model_combo.get()
        self.saved = True
        self.destroy()


class NHLTradeAnalyzerApp(ctk.CTk):
    """Main application window."""

    def __init__(self):
        super().__init__()

        self.title("NHL Trade Analyzer - AI Powered")
        self.geometry("1100x780")
        self.minsize(900, 650)
        self.configure(fg_color=BG_DARK)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.api_key = ""
        self.model = "gpt-4o"
        self.trade_history = []

        self._build_ui()

    def _build_ui(self):
        # Top bar
        top_bar = ctk.CTkFrame(self, fg_color=BG_CARD, height=56, corner_radius=0)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        ctk.CTkLabel(
            top_bar,
            text="🏒  NHL Trade Analyzer",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left", padx=20)

        ctk.CTkLabel(
            top_bar,
            text="AI-Powered Trade Analysis",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
        ).pack(side="left", padx=(4, 0))

        settings_btn = ctk.CTkButton(
            top_bar,
            text="⚙ Settings",
            font=ctk.CTkFont(size=13),
            fg_color=ACCENT_BLUE,
            hover_color="#1a4a7a",
            width=100,
            height=32,
            corner_radius=8,
            command=self._open_settings,
        )
        settings_btn.pack(side="right", padx=20)

        # Team selection bar
        team_bar = ctk.CTkFrame(self, fg_color=BG_DARK, height=50)
        team_bar.pack(fill="x", padx=16, pady=(12, 4))

        team_names = get_team_names()

        # Team 1 selector
        t1_frame = ctk.CTkFrame(team_bar, fg_color="transparent")
        t1_frame.pack(side="left", fill="x", expand=True, padx=(0, 8))

        ctk.CTkLabel(
            t1_frame,
            text="TEAM 1",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w")

        self.team1_var = ctk.CTkComboBox(
            t1_frame,
            values=team_names,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=14),
            height=36,
            command=self._on_team1_change,
        )
        self.team1_var.set(team_names[0])
        self.team1_var.pack(fill="x")

        # VS label
        ctk.CTkLabel(
            team_bar,
            text="⇄",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=ACCENT_HIGHLIGHT,
        ).pack(side="left", padx=12, pady=(12, 0))

        # Team 2 selector
        t2_frame = ctk.CTkFrame(team_bar, fg_color="transparent")
        t2_frame.pack(side="left", fill="x", expand=True, padx=(8, 0))

        ctk.CTkLabel(
            t2_frame,
            text="TEAM 2",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=TEXT_SECONDARY,
        ).pack(anchor="w")

        self.team2_var = ctk.CTkComboBox(
            t2_frame,
            values=team_names,
            fg_color=BG_INPUT,
            border_color=BORDER_COLOR,
            button_color=ACCENT_BLUE,
            dropdown_fg_color=BG_CARD,
            font=ctk.CTkFont(size=14),
            height=36,
            command=self._on_team2_change,
        )
        default_team2 = team_names[1] if len(team_names) > 1 else team_names[0]
        self.team2_var.set(default_team2)
        self.team2_var.pack(fill="x")

        # Main content area
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=16, pady=8)

        # Left panel - Trade Input
        left_panel = ctk.CTkFrame(content, fg_color="transparent")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))

        # Trade asset panels (side by side)
        trade_panels = ctk.CTkFrame(left_panel, fg_color="transparent")
        trade_panels.pack(fill="both", expand=True)

        initial_t1 = team_names[0]
        initial_t2 = default_team2

        self.team1_panel = TradeAssetFrame(
            trade_panels,
            initial_t1,
            get_team_color(initial_t1),
        )
        self.team1_panel.pack(side="left", fill="both", expand=True, padx=(0, 4))

        self.team2_panel = TradeAssetFrame(
            trade_panels,
            initial_t2,
            get_team_color(initial_t2),
        )
        self.team2_panel.pack(side="left", fill="both", expand=True, padx=(4, 0))

        # Action buttons
        btn_frame = ctk.CTkFrame(left_panel, fg_color="transparent", height=50)
        btn_frame.pack(fill="x", pady=(8, 0))

        self.analyze_btn = ctk.CTkButton(
            btn_frame,
            text="🔍  Analyze Trade",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=ACCENT_HIGHLIGHT,
            hover_color="#c93050",
            height=44,
            corner_radius=10,
            command=self._analyze_trade,
        )
        self.analyze_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑 Clear All",
            font=ctk.CTkFont(size=13),
            fg_color=ACCENT_BLUE,
            hover_color="#1a4a7a",
            height=44,
            width=110,
            corner_radius=10,
            command=self._clear_all,
        )
        self.clear_btn.pack(side="right", padx=(4, 0))

        # Right panel - Results
        right_panel = ctk.CTkFrame(content, fg_color=BG_CARD, corner_radius=12, width=380)
        right_panel.pack(side="right", fill="both", padx=(8, 0))
        right_panel.pack_propagate(False)

        results_header = ctk.CTkFrame(right_panel, fg_color="transparent")
        results_header.pack(fill="x", padx=16, pady=(12, 4))

        ctk.CTkLabel(
            results_header,
            text="Analysis Results",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left")

        self.status_label = ctk.CTkLabel(
            results_header,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=TEXT_SECONDARY,
        )
        self.status_label.pack(side="right")

        # Grade display
        self.grade_frame = ctk.CTkFrame(right_panel, fg_color=BG_INPUT, corner_radius=8, height=80)
        self.grade_frame.pack(fill="x", padx=16, pady=4)

        self.grade_team1_label = ctk.CTkLabel(
            self.grade_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        self.grade_team1_label.pack(side="left", padx=16, pady=8)

        self.grade_vs_label = ctk.CTkLabel(
            self.grade_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=TEXT_SECONDARY,
        )
        self.grade_vs_label.pack(side="left", expand=True)

        self.grade_team2_label = ctk.CTkLabel(
            self.grade_frame,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_SECONDARY,
        )
        self.grade_team2_label.pack(side="right", padx=16, pady=8)

        # Winner banner
        self.winner_label = ctk.CTkLabel(
            right_panel,
            text="",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=SUCCESS_GREEN,
        )
        self.winner_label.pack(fill="x", padx=16, pady=2)

        # Results text
        self.results_text = ctk.CTkTextbox(
            right_panel,
            fg_color=BG_INPUT,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(family="Consolas", size=12),
            corner_radius=8,
            wrap="word",
        )
        self.results_text.pack(fill="both", expand=True, padx=16, pady=(4, 8))
        self.results_text.insert("1.0", "Enter a trade and click 'Analyze Trade' to get started.\n\n"
                                        "Tips:\n"
                                        "• Add players with cap hit info for better analysis\n"
                                        "• Include draft picks and prospects\n"
                                        "• Set salary retention if applicable\n"
                                        "• Configure your OpenAI API key in Settings")
        self.results_text.configure(state="disabled")

        # History button
        self.history_btn = ctk.CTkButton(
            right_panel,
            text="📜  Trade History ({})".format(len(self.trade_history)),
            font=ctk.CTkFont(size=12),
            fg_color=ACCENT_BLUE,
            hover_color="#1a4a7a",
            height=32,
            corner_radius=8,
            command=self._show_history,
        )
        self.history_btn.pack(fill="x", padx=16, pady=(0, 12))

    def _on_team1_change(self, team_name):
        self.team1_panel.update_team(team_name, get_team_color(team_name))

    def _on_team2_change(self, team_name):
        self.team2_panel.update_team(team_name, get_team_color(team_name))

    def _open_settings(self):
        dialog = SettingsWindow(self, self.api_key, self.model)
        self.wait_window(dialog)
        if dialog.saved:
            self.api_key = dialog.api_key
            self.model = dialog.model

    def _analyze_trade(self):
        team1 = self.team1_var.get()
        team2 = self.team2_var.get()
        team1_assets = self.team1_panel.get_assets()
        team2_assets = self.team2_panel.get_assets()

        if not self.api_key:
            messagebox.showwarning(
                "API Key Required",
                "Please set your OpenAI API key in Settings before analyzing trades."
            )
            return

        if not team1_assets and not team2_assets:
            messagebox.showwarning(
                "No Assets",
                "Please add at least one asset to each side of the trade."
            )
            return

        if team1 == team2:
            messagebox.showwarning(
                "Same Team",
                "Please select two different teams for the trade."
            )
            return

        # Show loading state
        self.analyze_btn.configure(state="disabled", text="Analyzing...")
        self.status_label.configure(text="⏳ Analyzing...", text_color=WARNING_YELLOW)

        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "🤖 AI is analyzing your trade...\n\nThis may take a few seconds.")
        self.results_text.configure(state="disabled")

        # Run analysis in background thread
        thread = threading.Thread(
            target=self._run_analysis,
            args=(team1, team1_assets, team2, team2_assets),
            daemon=True,
        )
        thread.start()

    def _run_analysis(self, team1, team1_assets, team2, team2_assets):
        result = analyze_trade(
            self.api_key, team1, team1_assets, team2, team2_assets, self.model
        )

        # Update UI on main thread
        self.after(0, lambda: self._display_results(result, team1, team2))

    def _display_results(self, result, team1, team2):
        self.analyze_btn.configure(state="normal", text="🔍  Analyze Trade")

        if "error" in result:
            self.status_label.configure(text="❌ Error", text_color=ACCENT_HIGHLIGHT)
            self.results_text.configure(state="normal")
            self.results_text.delete("1.0", "end")
            self.results_text.insert("1.0", f"Error: {result['error']}")
            self.results_text.configure(state="disabled")
            self.grade_team1_label.configure(text="")
            self.grade_team2_label.configure(text="")
            self.grade_vs_label.configure(text="")
            self.winner_label.configure(text="")
            return

        # Update grades
        grade1 = result.get("trade_grade_team1", "?")
        grade2 = result.get("trade_grade_team2", "?")
        winner = result.get("winner", "")

        color1 = GRADE_COLORS.get(grade1, TEXT_PRIMARY)
        color2 = GRADE_COLORS.get(grade2, TEXT_PRIMARY)

        self.grade_team1_label.configure(
            text=f"{team1}: {grade1}",
            text_color=color1,
        )
        self.grade_vs_label.configure(text="vs", text_color=TEXT_SECONDARY)
        self.grade_team2_label.configure(
            text=f"{team2}: {grade2}",
            text_color=color2,
        )

        self.winner_label.configure(
            text=f"Winner: {winner}",
            text_color=SUCCESS_GREEN if winner != "Even" else WARNING_YELLOW,
        )

        # Format and display full analysis
        formatted = format_analysis_text(result, team1, team2)
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", formatted)
        self.results_text.configure(state="disabled")

        self.status_label.configure(text="✅ Complete", text_color=SUCCESS_GREEN)

        # Add to history
        self.trade_history.append({
            "team1": team1,
            "team2": team2,
            "grade1": grade1,
            "grade2": grade2,
            "winner": winner,
            "summary": result.get("summary", ""),
        })
        self.history_btn.configure(
            text="📜  Trade History ({})".format(len(self.trade_history))
        )

    def _clear_all(self):
        self.team1_panel.clear_assets()
        self.team2_panel.clear_assets()
        self.grade_team1_label.configure(text="")
        self.grade_team2_label.configure(text="")
        self.grade_vs_label.configure(text="")
        self.winner_label.configure(text="")
        self.status_label.configure(text="")
        self.results_text.configure(state="normal")
        self.results_text.delete("1.0", "end")
        self.results_text.insert("1.0", "Trade cleared. Add new assets to analyze.")
        self.results_text.configure(state="disabled")

    def _show_history(self):
        if not self.trade_history:
            messagebox.showinfo("Trade History", "No trades analyzed yet.")
            return

        history_win = ctk.CTkToplevel(self)
        history_win.title("Trade History")
        history_win.geometry("600x450")
        history_win.configure(fg_color=BG_DARK)

        ctk.CTkLabel(
            history_win,
            text="Trade History",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(pady=12)

        scroll = ctk.CTkScrollableFrame(history_win, fg_color=BG_INPUT, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        for i, trade in enumerate(reversed(self.trade_history), 1):
            card = ctk.CTkFrame(scroll, fg_color=BG_CARD, corner_radius=8)
            card.pack(fill="x", pady=4, padx=4)

            header = ctk.CTkLabel(
                card,
                text=f"Trade #{len(self.trade_history) - i + 1}: {trade['team1']} ⇄ {trade['team2']}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=TEXT_PRIMARY,
                anchor="w",
            )
            header.pack(fill="x", padx=12, pady=(8, 2))

            grades_text = f"Grades: {trade['team1']} {trade['grade1']} | {trade['team2']} {trade['grade2']} | Winner: {trade['winner']}"
            ctk.CTkLabel(
                card,
                text=grades_text,
                font=ctk.CTkFont(size=12),
                text_color=TEXT_SECONDARY,
                anchor="w",
            ).pack(fill="x", padx=12, pady=(0, 2))

            ctk.CTkLabel(
                card,
                text=trade.get("summary", ""),
                font=ctk.CTkFont(size=11),
                text_color=TEXT_SECONDARY,
                anchor="w",
                wraplength=540,
            ).pack(fill="x", padx=12, pady=(0, 8))
