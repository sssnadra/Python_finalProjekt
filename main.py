import random
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass


# ------------------------------------------------------------
# Klasse Player
# Speichert alle Daten, die zu einem einzelnen Spieler gehören.
# ------------------------------------------------------------
@dataclass
class Player:
    name: str
    score: int = 0
    rolls: int = 0
    ones_rolled: int = 0
    drink_rounds: int = 0
    failed_tests: int = 0
    active: bool = True

    def reset_score(self):
        """Setzt den aktuellen Punktestand des Spielers zurück."""
        self.score = 0

    def status_text(self):
        """Gibt den Status als Text für das Scoreboard zurück."""
        return "aktiv" if self.active else "ausgeschieden"


# ------------------------------------------------------------
# Klasse GameLogic
# Enthält die eigentliche Spiellogik ohne Tkinter-Code.
# ------------------------------------------------------------
class GameLogic:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.current_player_index = 0
        self.last_roll = None

    def get_current_player(self):
        """Gibt den aktuell aktiven Spieler zurück."""
        if not self.players:
            return None
        return self.players[self.current_player_index]

    def get_active_players(self):
        """Gibt alle Spieler zurück, die noch im Spiel sind."""
        return [player for player in self.players if player.active]

    def roll_number(self):
        """
        Würfelt eine Zahl von 1 bis 5 und wendet die Spielregeln an.

        Rückgabe:
        - rolled: gewürfelte Zahl
        - player: aktueller Spieler
        - sips: Anzahl Schlucke, falls eine 1 gewürfelt wurde
        - test_required: True, wenn ein Zungenbrecher-Test nötig ist
        """
        player = self.get_current_player()
        rolled = random.randint(1, 5)
        self.last_roll = rolled

        player.rolls += 1
        sips = 0
        test_required = False

        if rolled == 1:
            player.ones_rolled += 1
            sips = player.score
            player.drink_rounds += 1
            player.reset_score()

            # Jeder 5. Trinkrunde eines Spielers löst einen Test aus.
            if player.drink_rounds % 5 == 0:
                test_required = True
        else:
            player.score += rolled

        return {
            "rolled": rolled,
            "player": player,
            "sips": sips,
            "test_required": test_required
        }

    def move_to_next_player(self):
        """Wechselt zum nächsten aktiven Spieler."""
        if len(self.get_active_players()) <= 1:
            return

        start_index = self.current_player_index

        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

            if self.players[self.current_player_index].active:
                break

            # Sicherheit, damit keine Endlosschleife entstehen kann.
            if self.current_player_index == start_index:
                break

    def remove_player(self, player):
        """Entfernt einen Spieler aus dem aktiven Spiel."""
        player.active = False

        # Falls der entfernte Spieler gerade am Zug war, wird ein neuer aktiver Spieler gesucht.
        if self.players[self.current_player_index] == player:
            if len(self.get_active_players()) > 0:
                self.move_to_next_player()

    def has_winner(self):
        """Prüft, ob nur noch ein aktiver Spieler übrig ist."""
        return len(self.get_active_players()) == 1

    def get_winner(self):
        """Gibt den Gewinner zurück, falls es einen gibt."""
        active_players = self.get_active_players()
        if len(active_players) == 1:
            return active_players[0]
        return None


# ------------------------------------------------------------
# Klasse GameApp
# Verwaltet die komplette Tkinter-Oberfläche.
# ------------------------------------------------------------
class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecker, lecker Bierchen!")
        self.root.geometry("980x680")
        self.root.minsize(900, 600)

        self.game = None
        self.name_entries = []
        self.player_count_var = tk.IntVar(value=2)

        self.test_player = None
        self.test_attempt = 1

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        self.show_start_screen()

    # --------------------------------------------------------
    # Allgemeine Hilfsmethoden
    # --------------------------------------------------------
    def clear_screen(self):
        """Entfernt alle Widgets vom aktuellen Bildschirm."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def create_title(self, text):
        """Erstellt eine große Überschrift."""
        title = tk.Label(
            self.main_frame,
            text=text,
            font=("Arial", 24, "bold"),
            pady=15
        )
        title.pack()

    # --------------------------------------------------------
    # Startbildschirm
    # --------------------------------------------------------
    def show_start_screen(self):
        """Zeigt den Startbildschirm mit Spielernamen und Hinweistext."""
        self.clear_screen()
        self.game = None

        self.create_title("Lecker, lecker Bierchen!")

        subtitle = tk.Label(
            self.main_frame,
            text="Multiplayer-Zufallszahlenspiel mit Tkinter",
            font=("Arial", 13)
        )
        subtitle.pack(pady=(0, 15))

        settings_frame = tk.Frame(self.main_frame)
        settings_frame.pack(pady=5)

        tk.Label(settings_frame, text="Spieleranzahl:", font=("Arial", 11)).grid(row=0, column=0, padx=5)

        count_spinbox = tk.Spinbox(
            settings_frame,
            from_=2,
            to=6,
            width=5,
            textvariable=self.player_count_var,
            command=self.update_name_fields,
            state="readonly"
        )
        count_spinbox.grid(row=0, column=1, padx=5)

        update_button = tk.Button(
            settings_frame,
            text="Spielerfelder aktualisieren",
            command=self.update_name_fields
        )
        update_button.grid(row=0, column=2, padx=8)

        self.names_frame = tk.Frame(self.main_frame)
        self.names_frame.pack(pady=10)

        self.update_name_fields()

        hint_text = (
            "Obacht – dieses Spiel zählt zu den illustren Vergnügungen, bei denen gelegentlich "
            "Flüssigkeiten im Spiel sind. Alle Teilnehmenden sollten sich der möglichen Folgen "
            "bewusst sein und verantwortungsvoll handeln. Alkoholische Getränke dürfen ausschließlich "
            "von volljährigen Personen konsumiert werden. Bitte bedenkt: Alkohol ist ein Genussmittel "
            "und kein Spielzeug – übermäßiger Konsum kann der Gesundheit schaden."
        )

        hint_label = tk.Label(
            self.main_frame,
            text=hint_text,
            wraplength=850,
            justify="center",
            font=("Arial", 10),
            fg="#444444",
            padx=20,
            pady=15
        )
        hint_label.pack()

        start_button = tk.Button(
            self.main_frame,
            text="Spiel starten",
            font=("Arial", 14, "bold"),
            width=20,
            command=self.start_game
        )
        start_button.pack(pady=15)

        quit_button = tk.Button(
            self.main_frame,
            text="Spiel beenden",
            width=20,
            command=self.root.destroy
        )
        quit_button.pack()

    def update_name_fields(self):
        """Erstellt passend zur Spieleranzahl die Eingabefelder für Spielernamen."""
        for widget in self.names_frame.winfo_children():
            widget.destroy()

        self.name_entries = []

        try:
            count = int(self.player_count_var.get())
        except tk.TclError:
            count = 2
            self.player_count_var.set(2)

        for i in range(count):
            row_frame = tk.Frame(self.names_frame)
            row_frame.pack(pady=4)

            label = tk.Label(row_frame, text=f"Spieler {i + 1}:", width=12, anchor="e")
            label.pack(side="left", padx=5)

            entry = tk.Entry(row_frame, width=30)
            entry.pack(side="left", padx=5)
            entry.insert(0, f"Spieler {i + 1}")

            self.name_entries.append(entry)

    def validate_player_names(self):
        """Prüft leere oder doppelte Spielernamen."""
        names = []

        for entry in self.name_entries:
            name = entry.get().strip()

            if name == "":
                messagebox.showerror("Ungültige Eingabe", "Spielernamen dürfen nicht leer sein.")
                return None

            names.append(name)

        lower_names = [name.lower() for name in names]

        if len(lower_names) != len(set(lower_names)):
            messagebox.showerror("Ungültige Eingabe", "Spielernamen dürfen nicht doppelt vorkommen.")
            return None

        if len(names) < 2:
            messagebox.showerror("Ungültige Eingabe", "Es müssen mindestens 2 Spieler teilnehmen.")
            return None

        return names

    def start_game(self):
        """Startet ein neues Spiel mit den eingegebenen Spielern."""
        names = self.validate_player_names()

        if names is None:
            return

        self.game = GameLogic(names)
        self.show_game_screen()

    # --------------------------------------------------------
    # Spielbildschirm
    # --------------------------------------------------------
    def show_game_screen(self):
        """Zeigt den Hauptbildschirm des Spiels."""
        self.clear_screen()

        self.create_title("Lecker, lecker Bierchen!")

        self.current_player_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 16, "bold")
        )
        self.current_player_label.pack(pady=5)

        self.message_label = tk.Label(
            self.main_frame,
            text="Das Spiel beginnt. Riskier den Schluck!",
            font=("Arial", 12),
            wraplength=850,
            justify="center"
        )
        self.message_label.pack(pady=5)

        self.beer_label = tk.Label(
            self.main_frame,
            text="",
            font=("Arial", 50)
        )
        self.beer_label.pack(pady=5)

        self.create_scoreboard()

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=15)

        self.roll_button = tk.Button(
            button_frame,
            text="Riskier den Schluck",
            font=("Arial", 13, "bold"),
            width=22,
            command=self.handle_roll
        )
        self.roll_button.grid(row=0, column=0, padx=8)

        restart_button = tk.Button(
            button_frame,
            text="Neustart",
            width=18,
            command=self.restart_same_players
        )
        restart_button.grid(row=0, column=1, padx=8)

        new_players_button = tk.Button(
            button_frame,
            text="Neue Spieler einstellen",
            width=22,
            command=self.show_start_screen
        )
        new_players_button.grid(row=0, column=2, padx=8)

        quit_button = tk.Button(
            button_frame,
            text="Spiel beenden",
            width=18,
            command=self.root.destroy
        )
        quit_button.grid(row=0, column=3, padx=8)

        self.test_frame = tk.Frame(self.main_frame)
        self.test_frame.pack(pady=10)

        self.update_display()

    def create_scoreboard(self):
        """Erstellt das Live-Scoreboard als Tabelle."""
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = (
            "name",
            "score",
            "rolls",
            "ones",
            "drink_rounds",
            "failed_tests",
            "status"
        )

        self.scoreboard = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=9
        )

        self.scoreboard.heading("name", text="Spielername")
        self.scoreboard.heading("score", text="Score")
        self.scoreboard.heading("rolls", text="Würfe")
        self.scoreboard.heading("ones", text="1er")
        self.scoreboard.heading("drink_rounds", text="Trink-Runden")
        self.scoreboard.heading("failed_tests", text="Nicht bestandene Tests")
        self.scoreboard.heading("status", text="Status")

        self.scoreboard.column("name", width=160)
        self.scoreboard.column("score", width=80, anchor="center")
        self.scoreboard.column("rolls", width=80, anchor="center")
        self.scoreboard.column("ones", width=80, anchor="center")
        self.scoreboard.column("drink_rounds", width=120, anchor="center")
        self.scoreboard.column("failed_tests", width=160, anchor="center")
        self.scoreboard.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.scoreboard.yview
        )
        self.scoreboard.configure(yscrollcommand=scrollbar.set)

        self.scoreboard.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_display(self):
        """Aktualisiert aktiven Spieler und Scoreboard."""
        for row in self.scoreboard.get_children():
            self.scoreboard.delete(row)

        for player in self.game.players:
            self.scoreboard.insert(
                "",
                "end",
                values=(
                    player.name,
                    player.score,
                    player.rolls,
                    player.ones_rolled,
                    player.drink_rounds,
                    player.failed_tests,
                    player.status_text()
                )
            )

        current_player = self.game.get_current_player()

        if current_player is not None and current_player.active:
            self.current_player_label.config(
                text=f"It´s your turn: {current_player.name}"
            )
        else:
            self.current_player_label.config(text="Kein aktiver Spieler")

    def handle_roll(self):
        """Reagiert auf den Würfelbutton."""
        if self.game.has_winner():
            self.show_winner_screen()
            return

        self.clear_test_area()
        self.beer_label.config(text="")

        result = self.game.roll_number()
        player = result["player"]
        rolled = result["rolled"]
        sips = result["sips"]
        test_required = result["test_required"]

        if rolled == 1:
            self.beer_label.config(text="🍺")
            self.message_label.config(
                text=(
                    f"{player.name} hat eine 1 gewürfelt.\n"
                    f"Cheers! Lass es dir schmecken!\n"
                    f"{player.name} muss {sips} Schluck(e) trinken."
                )
            )

            if test_required:
                self.start_tongue_twister_test(player)
            else:
                self.game.move_to_next_player()
        else:
            self.message_label.config(
                text=(
                    f"{player.name} hat eine {rolled} gewürfelt.\n"
                    f"{rolled} Punkt(e) wurden addiert."
                )
            )
            self.game.move_to_next_player()

        self.update_display()

        if self.game.has_winner():
            self.show_winner_screen()

    def clear_test_area(self):
        """Entfernt alle Widgets des Zungenbrecher-Tests."""
        for widget in self.test_frame.winfo_children():
            widget.destroy()

    # --------------------------------------------------------
    # Zungenbrecher-Test
    # --------------------------------------------------------
    def start_tongue_twister_test(self, player):
        """Startet den Zungenbrecher-Test für einen Spieler."""
        self.test_player = player
        self.test_attempt = 1
        self.roll_button.config(state="disabled")
        self.show_test_widgets()

    def show_test_widgets(self):
        """Zeigt die Buttons und den Text für den Zungenbrecher-Test."""
        self.clear_test_area()

        tongue_twister = (
            "Auf den sieben Robbenklippen sitzen sieben Robbensippen, "
            "die sich in die Rippen stippen, bis sie von den Klippen kippen."
        )

        info_label = tk.Label(
            self.test_frame,
            text=(
                f"Zungenbrecher-Test für {self.test_player.name}!\n"
                f"Versuch {self.test_attempt} von 2\n\n"
                f"Bitte laut aufsagen:\n„{tongue_twister}“"
            ),
            font=("Arial", 12, "bold"),
            wraplength=850,
            justify="center"
        )
        info_label.pack(pady=8)

        button_frame = tk.Frame(self.test_frame)
        button_frame.pack()

        passed_button = tk.Button(
            button_frame,
            text="Bestanden!",
            width=18,
            command=self.test_passed
        )
        passed_button.grid(row=0, column=0, padx=8)

        failed_button = tk.Button(
            button_frame,
            text="Nicht bestanden!",
            width=18,
            command=self.test_failed
        )
        failed_button.grid(row=0, column=1, padx=8)

    def test_passed(self):
        """Behandelt einen bestandenen Zungenbrecher-Test."""
        self.message_label.config(
            text=f"{self.test_player.name}: still part oft he gamie!"
        )

        self.finish_test_and_continue()

    def test_failed(self):
        """Behandelt einen nicht bestandenen Testversuch."""
        self.test_player.failed_tests += 1

        if self.test_attempt == 1:
            self.test_attempt = 2
            self.message_label.config(text="Let's try again!")
            self.show_test_widgets()
        else:
            self.show_remove_player_option()

        self.update_display()

    def show_remove_player_option(self):
        """Zeigt nach zwei Fehlversuchen die Option zum Entfernen des Spielers."""
        self.clear_test_area()

        self.message_label.config(
            text=(
                f"{self.test_player.name}: I glaub, du bist voll wie eine Haubitze."
            )
        )

        info_label = tk.Label(
            self.test_frame,
            text=f"Soll {self.test_player.name} aus dem Spiel entfernt werden?",
            font=("Arial", 12, "bold")
        )
        info_label.pack(pady=8)

        button_frame = tk.Frame(self.test_frame)
        button_frame.pack()

        remove_button = tk.Button(
            button_frame,
            text="Spieler entfernen",
            width=20,
            command=self.remove_test_player
        )
        remove_button.grid(row=0, column=0, padx=8)

        keep_button = tk.Button(
            button_frame,
            text="Weiterspielen lassen",
            width=20,
            command=self.finish_test_and_continue
        )
        keep_button.grid(row=0, column=1, padx=8)

    def remove_test_player(self):
        """Entfernt den Spieler nach nicht bestandenem Test aus dem Spiel."""
        self.game.remove_player(self.test_player)

        self.message_label.config(
            text=f"{self.test_player.name} wurde aus dem Spiel entfernt."
        )

        self.clear_test_area()
        self.roll_button.config(state="normal")
        self.update_display()

        if self.game.has_winner():
            self.show_winner_screen()

    def finish_test_and_continue(self):
        """Beendet den Test und wechselt zum nächsten aktiven Spieler."""
        self.clear_test_area()
        self.roll_button.config(state="normal")

        if self.test_player is not None and self.test_player.active:
            self.game.move_to_next_player()

        self.test_player = None
        self.test_attempt = 1

        self.update_display()

        if self.game.has_winner():
            self.show_winner_screen()

    # --------------------------------------------------------
    # Neustart und Spielende
    # --------------------------------------------------------
    def restart_same_players(self):
        """Startet das Spiel mit denselben Spielernamen neu."""
        if self.game is None:
            self.show_start_screen()
            return

        names = [player.name for player in self.game.players]
        self.game = GameLogic(names)
        self.show_game_screen()

    def show_winner_screen(self):
        """Zeigt die Gewinner-Meldung und beendet die Runde."""
        winner = self.game.get_winner()

        if winner is None:
            return

        self.clear_screen()

        self.create_title("Spiel beendet!")

        winner_label = tk.Label(
            self.main_frame,
            text=f"Gewonnen hat: {winner.name}",
            font=("Arial", 22, "bold"),
            fg="green"
        )
        winner_label.pack(pady=15)

        summary_label = tk.Label(
            self.main_frame,
            text="Nur noch ein Spieler ist aktiv. Das Spiel endet automatisch.",
            font=("Arial", 12)
        )
        summary_label.pack(pady=5)

        self.create_final_scoreboard()

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        restart_button = tk.Button(
            button_frame,
            text="Neu starten",
            width=18,
            command=self.restart_same_players
        )
        restart_button.grid(row=0, column=0, padx=8)

        new_players_button = tk.Button(
            button_frame,
            text="Neue Spieler einstellen",
            width=22,
            command=self.show_start_screen
        )
        new_players_button.grid(row=0, column=1, padx=8)

        quit_button = tk.Button(
            button_frame,
            text="Beenden",
            width=18,
            command=self.root.destroy
        )
        quit_button.grid(row=0, column=2, padx=8)

    def create_final_scoreboard(self):
        """Zeigt am Ende noch einmal die vollständige Tabelle."""
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill="both", expand=True, padx=20, pady=15)

        columns = (
            "name",
            "score",
            "rolls",
            "ones",
            "drink_rounds",
            "failed_tests",
            "status"
        )

        final_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        final_table.heading("name", text="Spielername")
        final_table.heading("score", text="Score")
        final_table.heading("rolls", text="Würfe")
        final_table.heading("ones", text="1er")
        final_table.heading("drink_rounds", text="Trink-Runden")
        final_table.heading("failed_tests", text="Nicht bestandene Tests")
        final_table.heading("status", text="Status")

        final_table.column("name", width=160)
        final_table.column("score", width=80, anchor="center")
        final_table.column("rolls", width=80, anchor="center")
        final_table.column("ones", width=80, anchor="center")
        final_table.column("drink_rounds", width=120, anchor="center")
        final_table.column("failed_tests", width=160, anchor="center")
        final_table.column("status", width=120, anchor="center")

        final_table.pack(fill="both", expand=True)

        for player in self.game.players:
            final_table.insert(
                "",
                "end",
                values=(
                    player.name,
                    player.score,
                    player.rolls,
                    player.ones_rolled,
                    player.drink_rounds,
                    player.failed_tests,
                    player.status_text()
                )
            )


# ------------------------------------------------------------
# Programmstart
# ------------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()