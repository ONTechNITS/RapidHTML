from rapidhtml.style import StyleSheet

stylesheet = {
    ".styled-table": {
        "border-collapse": "collapse",
        "margin": "25px 0",
        "font-size": "0.9em",
        "min-width": "400px",
        "box-shadow": "0 0 20px rgba(0, 0, 0, 0.15)",
    },
    ".styled-table": {
        "thead": {
            "tr": {
                "background-color": "#009879",
                "color": "#ffffff",
                "text-align": "left",
            }
        },
        "th": {"padding": "12px 15px"},
        "td": {"padding": "12px 15px"},
        "tbody": {
            "tr": {"border-bottom": "1px solid #dddddd"},
            "tr:nth-of-type(even)": {"background-color": "#f3f3f3"},
            "tr:last-of-type": {"border-bottom": "2px solid #009879"},
        },
    },
}

table_styling = StyleSheet(**stylesheet)

__all__ = ["table_styling"]
