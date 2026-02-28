"""NHL team and player data for the trade analyzer."""

# NHL Teams with their divisions, conferences, and primary colors
NHL_TEAMS = {
    "Anaheim Ducks": {"abbr": "ANA", "conference": "Western", "division": "Pacific", "color": "#F47A38"},
    "Arizona Coyotes": {"abbr": "ARI", "conference": "Western", "division": "Central", "color": "#8C2633"},
    "Boston Bruins": {"abbr": "BOS", "conference": "Eastern", "division": "Atlantic", "color": "#FFB81C"},
    "Buffalo Sabres": {"abbr": "BUF", "conference": "Eastern", "division": "Atlantic", "color": "#002654"},
    "Calgary Flames": {"abbr": "CGY", "conference": "Western", "division": "Pacific", "color": "#D2001C"},
    "Carolina Hurricanes": {"abbr": "CAR", "conference": "Eastern", "division": "Metropolitan", "color": "#CC0000"},
    "Chicago Blackhawks": {"abbr": "CHI", "conference": "Western", "division": "Central", "color": "#CF0A2C"},
    "Colorado Avalanche": {"abbr": "COL", "conference": "Western", "division": "Central", "color": "#6F263D"},
    "Columbus Blue Jackets": {"abbr": "CBJ", "conference": "Eastern", "division": "Metropolitan", "color": "#002654"},
    "Dallas Stars": {"abbr": "DAL", "conference": "Western", "division": "Central", "color": "#006847"},
    "Detroit Red Wings": {"abbr": "DET", "conference": "Eastern", "division": "Atlantic", "color": "#CE1126"},
    "Edmonton Oilers": {"abbr": "EDM", "conference": "Western", "division": "Pacific", "color": "#041E42"},
    "Florida Panthers": {"abbr": "FLA", "conference": "Eastern", "division": "Atlantic", "color": "#041E42"},
    "Los Angeles Kings": {"abbr": "LAK", "conference": "Western", "division": "Pacific", "color": "#111111"},
    "Minnesota Wild": {"abbr": "MIN", "conference": "Western", "division": "Central", "color": "#154734"},
    "Montreal Canadiens": {"abbr": "MTL", "conference": "Eastern", "division": "Atlantic", "color": "#AF1E2D"},
    "Nashville Predators": {"abbr": "NSH", "conference": "Western", "division": "Central", "color": "#FFB81C"},
    "New Jersey Devils": {"abbr": "NJD", "conference": "Eastern", "division": "Metropolitan", "color": "#CE1126"},
    "New York Islanders": {"abbr": "NYI", "conference": "Eastern", "division": "Metropolitan", "color": "#00539B"},
    "New York Rangers": {"abbr": "NYR", "conference": "Eastern", "division": "Metropolitan", "color": "#0038A8"},
    "Ottawa Senators": {"abbr": "OTT", "conference": "Eastern", "division": "Atlantic", "color": "#C52032"},
    "Philadelphia Flyers": {"abbr": "PHI", "conference": "Eastern", "division": "Metropolitan", "color": "#F74902"},
    "Pittsburgh Penguins": {"abbr": "PIT", "conference": "Eastern", "division": "Metropolitan", "color": "#FCB514"},
    "San Jose Sharks": {"abbr": "SJS", "conference": "Western", "division": "Pacific", "color": "#006D75"},
    "Seattle Kraken": {"abbr": "SEA", "conference": "Western", "division": "Pacific", "color": "#001628"},
    "St. Louis Blues": {"abbr": "STL", "conference": "Western", "division": "Central", "color": "#002F87"},
    "Tampa Bay Lightning": {"abbr": "TBL", "conference": "Eastern", "division": "Atlantic", "color": "#002868"},
    "Toronto Maple Leafs": {"abbr": "TOR", "conference": "Eastern", "division": "Atlantic", "color": "#00205B"},
    "Utah Hockey Club": {"abbr": "UTA", "conference": "Western", "division": "Central", "color": "#71AFE5"},
    "Vancouver Canucks": {"abbr": "VAN", "conference": "Western", "division": "Pacific", "color": "#00205B"},
    "Vegas Golden Knights": {"abbr": "VGK", "conference": "Western", "division": "Pacific", "color": "#B4975A"},
    "Washington Capitals": {"abbr": "WSH", "conference": "Eastern", "division": "Metropolitan", "color": "#041E42"},
    "Winnipeg Jets": {"abbr": "WPG", "conference": "Western", "division": "Central", "color": "#041E42"},
}

POSITIONS = ["C", "LW", "RW", "D", "G"]

DRAFT_PICKS = [
    "2025 1st Round Pick",
    "2025 2nd Round Pick",
    "2025 3rd Round Pick",
    "2025 4th Round Pick",
    "2025 5th Round Pick",
    "2025 6th Round Pick",
    "2025 7th Round Pick",
    "2026 1st Round Pick",
    "2026 2nd Round Pick",
    "2026 3rd Round Pick",
    "2026 4th Round Pick",
    "2026 5th Round Pick",
    "2026 6th Round Pick",
    "2026 7th Round Pick",
    "2027 1st Round Pick",
    "2027 2nd Round Pick",
    "2027 3rd Round Pick",
    "2027 4th Round Pick",
    "2027 5th Round Pick",
    "2027 6th Round Pick",
    "2027 7th Round Pick",
    "2028 1st Round Pick",
    "2028 2nd Round Pick",
    "2028 3rd Round Pick",
    "Conditional Pick",
]

SALARY_RETENTION_OPTIONS = ["0%", "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%"]


def get_team_names():
    """Return sorted list of NHL team names."""
    return sorted(NHL_TEAMS.keys())


def get_team_color(team_name):
    """Return the primary color for a team."""
    if team_name in NHL_TEAMS:
        return NHL_TEAMS[team_name]["color"]
    return "#1a1a2e"


def get_team_abbr(team_name):
    """Return the abbreviation for a team."""
    if team_name in NHL_TEAMS:
        return NHL_TEAMS[team_name]["abbr"]
    return ""


def get_team_info(team_name):
    """Return full info dict for a team."""
    return NHL_TEAMS.get(team_name, {})
