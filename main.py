from st_pages import Page, Section, add_page_title, show_pages

show_pages(
    [
        Page("menu/dashboard.py", "Dashboard", "⚒"),
        Section(name="Loader", icon=":apple:"),
        Page("menu/loader_performances.py", "Loader Performances", "🦿"),
        Page("menu/loader_status.py", "Loader Status", "🦵"),
        Section(name="Hauler", icon=":banana:"),
        Page("menu/hauler_performances.py", "Hauler Performances", "🦾"),
        Page("menu/hauler_status.py", "Hauler Status", "💪"),
        Page("menu/logs.py", "Log Data", "🧲", in_section=False),
        Page("menu/locations.py", "Location", "📌", in_section=False)
    ]
)

add_page_title()