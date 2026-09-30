"""The full GUI for the Steam Search engine, handles all stylistic and 
functional textboxes, buttons, windows, etc."""
import tkinter as tk

from connector import FirebaseConnector
from tkinter import ttk

# steam-style color palette
BG_COLOR = "#171D29"
PANEL_COLOR = "#252F40"
INPUT_COLOR = "#101722"
ACCENT_COLOR = "#66C0F4"
TEXT_COLOR = "#E5EAF0"
MUTED_TEXT_COLOR = "#9EAAB9"
SEARCH_BG_COLOR = "#2B3A4D"
BORDER_COLOR = "#4A6A85"
SECONDARY_BUTTON_COLOR = "#34465B"

# steam font
FONT_FAMILY = "Segoe UI"
TITLE_FONT = (FONT_FAMILY, 24, "bold")
TITLE_FONT_HELP = (FONT_FAMILY, 17, "bold")
BUTTON_FONT = (FONT_FAMILY, 11, "bold")
BODY_FONT = (FONT_FAMILY, 11)
INPUT_FONT = (FONT_FAMILY, 12)

"""Gets an instance of the Firestore connection and 
returns a ready-to-use version"""
def get_FB_instance():
    connector = FirebaseConnector()
    db = connector.get_database()
    return db

"""Sets up the main window itsself so widgets can be added."""
def create_window():
    root = tk.Tk()
    root.title("Steam Search")
    root. geometry("800x600")

    root.configure(bg=BG_COLOR)

    return root

"""Extra style stuff for the scrollbar in the results box"""
def configure_scrollbar_style():
    style = ttk.Style()

    style.theme_use("clam")

    style.configure(
        "Steam.Vertical.TScrollbar",
        background=SECONDARY_BUTTON_COLOR,
        troughcolor=BG_COLOR,
        bordercolor=BG_COLOR,
        arrowcolor=TEXT_COLOR,
        darkcolor=SECONDARY_BUTTON_COLOR,
        lightcolor=SECONDARY_BUTTON_COLOR,
        relief="flat",
        borderwidth=0,
        arrowsize=10,
        width=12
    )

    style.map(
        "Steam.Vertical.TScrollbar",
        background=[
            ("active", ACCENT_COLOR),
            ("pressed", ACCENT_COLOR)
        ]
    )

"""Sets up the main window and widgets of the GUI"""
def create_widgets(root, db):
    # title
    title_label = tk.Label(
        root,
        text="Steam Search",
        font=TITLE_FONT,
        bg=BG_COLOR,
        fg=ACCENT_COLOR
    )

    title_label.grid(
        row=0,
        column=0,
        columnspan=2,
        padx=20,
        pady=(20, 10)
    )

    # search box
    query_entry = tk.Entry(
        root,
        width=40,
        font=INPUT_FONT,
        bg=SEARCH_BG_COLOR,
        fg=TEXT_COLOR,
        insertbackground=ACCENT_COLOR,
        relief="solid",
        bd=1,
        highlightthickness=1,
        highlightbackground=BORDER_COLOR,
        highlightcolor=ACCENT_COLOR
    )

    query_entry.grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="ew"
    )

    query_entry.focus_set()

    # results box
    results_frame = tk.Frame(
        root,
        bg=PANEL_COLOR
    )

    results_frame.grid(
        row=2,
        column=0,
        columnspan=2,
        padx=10,
        pady=10,
        sticky="nsew"
    )

    results_frame.rowconfigure(0, weight=1)
    results_frame.columnconfigure(0, weight=1)

    results_box = tk.Text(
        results_frame,
        width=50,
        height=15,
        wrap="word",
        font=BODY_FONT,
        bg=PANEL_COLOR,
        fg=TEXT_COLOR,
        insertbackground=ACCENT_COLOR,
        selectbackground=ACCENT_COLOR,
        selectforeground=BG_COLOR,
        relief="solid",
        bd=1,
        padx=12,
        pady=10
    )

    results_box.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    results_scrollbar = ttk.Scrollbar(
        results_frame,
        orient="vertical",
        command=results_box.yview,
        style="Steam.Vertical.TScrollbar"
    )

    results_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    results_box.configure(
        yscrollcommand=results_scrollbar.set,
        state="disabled"
    )

    # search button
    search_button = tk.Button(
        root,
        text="Search",
        command=lambda: get_and_process_query(query_entry, results_box, db),
        font=BUTTON_FONT,
        bg=ACCENT_COLOR,
        fg=BG_COLOR,
        activebackground="#8BD3FF",
        activeforeground=BG_COLOR,
        relief="flat",
        bd=0,
        padx=10,
        pady=3,
        cursor="hand2"
    )

    search_button.grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )

    # help button
    help_button = tk.Button(
        root,
        text="Help",
        command=lambda: open_help_window(root),
        font=BUTTON_FONT,
        bg=SECONDARY_BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground="#465D76",
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        padx=10,
        pady=3,
        cursor="hand2"
    )

    help_button.grid(
        row=3,
        column=0,
        padx=10,
        pady=10,
        sticky="w"
    )

    # quit button
    quit_button = tk.Button(
        root,
        text="Quit",
        command=root.destroy,
        font=BUTTON_FONT,
        bg=SECONDARY_BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground="#465D76",
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        padx=10,
        pady=3,
        cursor="hand2"
    )

    quit_button.grid(
        row=3,
        column=1,
        padx=10,
        pady=10,
        sticky="e"
    )

    root.columnconfigure(0, weight=1)
    root.rowconfigure(2, weight=1)
    

"""Opens and configures the help window."""
def open_help_window(root):
    help_window = tk.Toplevel(root)

    help_window.title("Help")
    help_window.geometry("800x600")

    help_window.configure(bg=BG_COLOR)

    heading = tk.Label(
        help_window,
        text="Query Syntax Help",
        font=TITLE_FONT_HELP,
        bg=BG_COLOR,
        fg=ACCENT_COLOR
    )

    heading.pack(pady=(20, 10))

    instructions = tk.Label(
        help_window,
        text=(
            """Valid fields: app_id, name, release_date, price, metacritic_url, categories, genres, tags
                    Valid operators: =, !=, <, >, <=, >=

                To search, use the following syntax:

                    (field)(operator)(value) will return all games that satisfy the condition
                    (field)(operator)(value) and (field)(operator)(value) will return all games that satisfy both 
                        conditions.
                    (field)(operator)(value) (field)(operator)(value) will do the same.
                    (field)(operator)(value) or (field)(operator)(value) will return all games that satisfy at least one 
                        condition.

                Examples queries:
                    price<9.99 will return all games that cost less than $9.99.
                    price<9.99 and release_date=2023-09-21 will return all games released on 9/21/23 that cost 
                        less than $9.99.
                    price<9.99 release_date=2023-09-21 will behave identically.
                    price<9.99 or release_date=2023-09-21 will return all games that either
                        were released on 9/21/23 or cost less than $9.99."""
        ),
        font=BODY_FONT,
        bg=BG_COLOR,
        fg=TEXT_COLOR,
        justify="left",
        anchor="w"
    )

    instructions.pack(
        padx=30,
        pady=10,
        anchor="w"
    )

    dismiss_button = tk.Button(
        help_window,
        text="Dismiss",
        command=help_window.destroy,
        font=BUTTON_FONT,
        bg=SECONDARY_BUTTON_COLOR,
        fg=TEXT_COLOR,
        activebackground="#465D76",
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=0,
        padx=10,
        pady=3,
        cursor="hand2"
    )

    dismiss_button.pack(
        side="bottom",
        anchor="e",
        padx=20,
        pady=20
    )


# collect query from textbox
# send query to parser
# display results?
def get_and_process_query(query_entry, results_box, db):
    # call parser
    # call do query
    # call display results? or do it here

    ## query = query_entry.get().strip()
    ## parsed_q = parse_query(query)

    ## do_query(db, parsed_q) --- must return whether query is okay?
    ## query_check, results = do_query(^)
    ## if(query_check):
    ##      display_results(results_box, results)
    ## else:
    ##      bad_query(results_box)

    #results = {"key": "value",
     #            "key2": "value"}
    #isplay_results(results_box, results)
     #!!!!strings display test passed
     #!!!! dictionary works but brackets print
    pass

"""Display text in the read-only results box."""
def display_results(results_box, text):
    results_box.config(state="normal")

    results_box.delete("1.0", tk.END)

    results_box.insert(tk.END, text)

    results_box.config(state="disabled")

"""Displays message about bad query, points user to help window"""
def bad_query(results_box):
    error_text = (
        "Invalid query.\n\n"
        "Click the Help button for information about valid queries."
    )
    display_results(results_box, error_text)

def main():
    root = create_window()

    # db = get_FB_instance()
    db = []

    configure_scrollbar_style()

    create_widgets(root, db)

    root.mainloop()

if __name__ == "__main__":
    main()

