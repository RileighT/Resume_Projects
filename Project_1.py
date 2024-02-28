import pandas as pd 
import re
import sqlite3
from argparse import ArgumentParser
import sys

# Dictionary mapping team codes to team names
nhl_teams = {"ANH":"Anaheim Ducks","ARI":"Arizona Coyotes","BOS":"Boston Bruins","BUF":"Buffalo Sabres","CGY":"Calgary Flames",\
        "CAR":"Carolina Hurricanes","CHI":"Chicago Blackhawks","COL":"Colorado Avalanche","CLS":"Columbus Blue Jackets",\
        "DAL":"Dallas Stars","DET":"Detroit Red Wings","EDM":"Edmonton Oilers","FLA":"Florida Panthers","LA":"Los Angeles Kings",\
        "MIN":"Minnesota Wild","MON":"Montreal Canadiens","NSH":"Nashville Predators","NJ":"New Jersey Devils","NYI":"New York Islanders",\
        "NYR":"New York Rangers","OTT":"Ottawa Senators","PHI":"Philadelphia Flyers","PIT":"Pittsburgh Penguins","SJ":"San Jose Sharks",\
        "SEA":"Seattle Kraken","STL":"St. Louis Blues","TB":"Tampa Bay Lightning","TOR":"Toronto Maple Leafs","VAN":"Vancouver Canucks",\
        "VGK":"Vegas Golden Knights","WAS":"Washington Capitals","WPG":"Winnipeg Jets"}

class Player:
    """
    A class that represents an NHL player.

    Attributes:
    - name (str): The name of the player.
    - team (str): The team to which the player belongs.
    - position (str): The playing position of the player (e.g., Forward, Defense).
    - goals (int): The number of goals scored by the player.
    - penalty_minutes (int): The total penalty minutes accumulated by the player.

    Methods:
    - None
    """
    def __init__(self, name, team, position, goals, penalty_minutes):
        self.name = name
        self.team = team
        self.position = position
        self.goals = goals
        self.penalty_minutes = penalty_minutes

class Team:
    """
    A class that represents an NHL team.

    Attributes:
    - name (str): The name of the team.
    - players (list): A list of Player objects representing the team's players.

    Methods:
    - None
    """
    def __init__(self, name, players):
        self.name = name
        self.players = players
 

class PlayerHandler:
    """
    A class for handling NHL player data, including skaters and goalies.

    Attributes:
    None

    Methods:
    - read_skaters_data(file_path): Reads skaters data from a CSV file.
    - filter_skaters_by_position(skaters, position): Filters skaters based on their playing position.
    - calculate_points(skaters): Calculates total points for each skater.
    - top_players_by_points(skaters, num_players=10): Returns the top players based on points.
    - read_goalies_data(file_path): Reads goalies data from a CSV file.
    - calculate_save_percentage(goalies): Calculates save percentage for each goalie.
    - top_goalies_by_save_percentage(goalies, num_goalies=5): Returns the top goalies based on save percentage.
    """
    def __init__(self,df):
        self.df = df
        self.names = []
        self.df['Team Name'] = df['Team'].map(nhl_teams)


    def read_skaters_data(self,file_path):
        """
        Reads skaters data from a CSV file.

        Parameters:
        - file_path (str): The path to the CSV file containing skaters data.

        Returns:
        - A DataFrame containing skaters data.
        """
        skaters = pd.read_csv(file_path)
        return skaters

    def filter_skaters_by_position(self, skaters, position):
        """
        Filters skaters based on their playing position.

        Parameters:
        - skaters (pandas.DataFrame): DataFrame containing skaters data.
        - position (str): The playing position to filter by.

        Returns:
        - A filtered DataFrame containing skaters with the specified position.
        """
        # Using boolean indexing to filter skaters based on the specified position
        return skaters[skaters['Pos'] == position]

    def top_players_by_goals(self,num_players=5):
        """
        Returns the top players based on points.

        Parameters:
        - num_players (int): The number of top players to return.

        Returns:
        - The top players based on points.
        """
        # Sort skaters DataFrame by the 'G' (goals) column in descending order
        sorted_skaters = self.df.sort_values(by=['G'], ascending=[False])
        self.names.append(sorted_skaters['Player Name'].head(num_players)) 

        # Return the first 'num_players' rows from the sorted DataFrame
        return sorted_skaters.head(num_players)

    def read_goalies_data(self,file_path):
        """
        Reads goalies data from a CSV file.

        Parameters:
        - file_path (str): The path to the CSV file containing goalies data.

        Returns:
        - A DataFrame containing goalies data.
        """
        goalies = pd.read_csv(file_path)
        return goalies

    def calculate_save_percentage(self,goalies):
        """
        Calculates save percentage for each goalie.

        Parameters:
        - goalies (pandas.DataFrame): DataFrame containing goalies data.

        Returns:
        - A DataFrame with an additional 'Save Percentage' column.
        """
        # Calculate save percentage by dividing 'SV' (saves) by 'SA' (shots against)
        goalies['SavePercentage'] = goalies['SV'] / goalies['SA']
        # Return a DataFrame with 'Player Name' and 'Save Percentage' columns
        return goalies[['Player Name', 'SavePercentage']]

    def top_goalies_by_save_percentage(self,num_goalies=5):
        """
        Returns the top goalies based on save percentage.

        Parameters:
        - num_goalies (int): The number of top goalies to return.

        Returns:
        - The top goalies based on save percentage.
        """
        # Sort the goalies DataFrame by 'SV%' (save percentage) in descending order
        sorted_goalies = self.df.sort_values(by='SV%', ascending=False)
        # Return the top 'num_goalies' goalies from the sorted DataFrame
        return sorted_goalies.head(num_goalies)
    
    def top_players_by_hits(self, num_players=10):
        """
        Returns the top players based on hits.

        Parameters:
        - num_players (int): The number of top players to return.

        Returns:
        - A DataFrame with the top players based on hits.
        """
        # Sort skaters DataFrame by 'Hits' column in descending order
        sorted_skaters = self.df.sort_values(by='Hits', ascending=False)
        # Return the top 'num_players' players based on hits
        return sorted_skaters.head(num_players)

    def top_players_by_pim(self, num_players=10):
        """
        Returns the top players based on penalty minutes.

        Parameters:
        - num_players (int): The number of top players to return.

        Returns:
        - A DataFrame with the top players based on penalty minutes.
        """
        # Sort skaters DataFrame by 'PIM' (Penalty Minutes) column in descending order
        sorted_skaters = self.df.sort_values(by='PIM', ascending=False)
        # Return the top 'num_players' players based on penalty minutes
        return sorted_skaters.head(num_players)
    
    def get_player_info(self):
        return self.names


class Goalie(Player):
    """
    A class that represents an NHL goalie.

    Attributes:
    - name (str): The name of the goalie.
    - country (str): The country of origin of the goalie.
    - saves (int): The number of saves made by the goalie.
    - goals_allowed (int): The number of goals allowed by the goalie.

    Methods:
    - None
    """

    def __init__(self, name, country, saves, goals_allowed):
        """
        Initializes a Goalie object.

        Parameters:
        - name (str): The name of the goalie.
        - country (str): The country of origin of the goalie.
        - saves (int): The number of saves made by the goalie.
        - goals_allowed (int): The number of goals allowed by the goalie.

        Returns:
        None
        """
        # Call the constructor of the parent class (Player) with specific goalie attributes
        super().__init__(name, country, position="Goalie", goals=0, penalty_minutes=0)
        # Set additional attributes specific to Goalie
        self.saves = saves
        self.goals_allowed = goals_allowed


class Team:
    """
    A class for handling NHL team-related functionalities.

    Methods:
    - extract_team_code(player_info): Extracts the team code from player information.

    Attributes:
    - None
    """

    def extract_team_code(player_info):
        """
        Extracts the team code from player information.

        Parameters:
        - player_info (str): Player information containing the team code in parentheses.

        Returns:
        - str: The extracted team code if found, or None if not found.
        """
        # Use a regular expression to search for a team code in parentheses
        match = re.search(r'\(([A-Z]+)\)', player_info)
        if match:
            # If a match is found, return the extracted team code
            return match.group(1)
        else:
            # If no match is found, return None
            return None


#module 9 - GIT Hub. I am incoperating this module by uplaoding my progress and final into git hub


class DataHandler:
    """
    A class for handling NHL data and creating Pandas DataFrames.

    Methods:
    - create_dataframe(players): Creates a Pandas DataFrame from a list of player objects.

    Attributes:
    - None
    """

    def create_dataframe(players):
        """
        Creates a Pandas DataFrame from a list of player objects.

        Parameters:
        - players (list): A list of Player objects.

        Returns:
        - pandas.DataFrame: A DataFrame containing player data.
        """
        # Use Pandas to create a DataFrame from the list of player objects
        return pd.DataFrame(players)


class SQL:
    """
    A class for handling SQL operations related to NHL player data.

    Methods:
    - create_database(players): Creates an SQLite database and inserts player data.

    Attributes:
    - None
    """

    def create_database(players):
        """
        Creates an SQLite database and inserts player data.

        Parameters:
        - players (list): A list of Player objects.

        Returns:
        - None
        """
        # Connect to the SQLite database (or create if it doesn't exist)
        conn = sqlite3.connect('nhl_players.db')
        # Create a cursor to execute SQL commands
        c = conn.cursor()

        # Create a table if it doesn't exist with columns: name, team, position, goals, penalty_minutes
        c.execute('CREATE TABLE IF NOT EXISTS players (name TEXT, team TEXT, position TEXT, goals INTEGER, penalty_minutes INTEGER)')

        # Insert player data into the 'players' table
        for player in players:
            c.execute('INSERT INTO players VALUES (?, ?, ?, ?, ?)', (player.name, player.team, player.position, player.goals, player.penalty_minutes))

        # Commit the changes to the database and close the connection
        conn.commit()
        conn.close()


def goal_scorers_analysis(sdf, num):
    """
    Analyzes skaters' data and prints the top goal scorers.

    Parameters:
    - sdf (pandas.DataFrame): DataFrame containing skaters' data.
    - num (int): The number of top goal scorers to display.

    Returns:
    - names list
    """
    # Create a PlayerHandler instance
    players = PlayerHandler(sdf)
    # Get the top goal scorers using the PlayerHandler instance
    top_scorers = players.top_players_by_goals(num)
    # Sort the top scorers DataFrame by goals (G) in descending order
    sorted_top_scorers = top_scorers.sort_values(by='G', ascending=False)
    sorted_top_scorers.index = range(1,len(sorted_top_scorers) + 1)
    # Print information about the top goal scorers
    print(f"\nTop {num} Goal Scorers:")
    for index, row in sorted_top_scorers.iterrows():
        print(f"Top scorer #:{index} {row['Player Name']} from {row['Team Name']} scored {row['G']} goals.")
    return players

def goalies_analysis(gdf, num):
    """
    Analyzes goalies' data and prints the top goalies based on save percentage.

    Parameters:
    - gdf (pandas.DataFrame): DataFrame containing goalies' data.
    - num (int): The number of top goalies to display.

    Returns:
    - names list
    """
    # Create a PlayerHandler instance for goalies
    goalies = PlayerHandler(gdf)
    # Get the top goalies based on save percentage using the PlayerHandler instance
    top_goalies = goalies.top_goalies_by_save_percentage(num)
    top_goalies.index = range(1,len(top_goalies) + 1)
    # Sort the top goalies DataFrame by save percentage (SV%) in descending order
    top_goalies = top_goalies.sort_values(by='SV%', ascending=False)
    for index, row in top_goalies.iterrows():
        print(f"Top Goalie #:{index} {row['Player Name']} from {row['Team Name']} has {row['SV%']} save percentage.")
    return goalies


def hitters_analysis(sdf, num):
    """
    Analyzes skaters' data and prints the top hitters.

    Parameters:
    - sdf (pandas.DataFrame): DataFrame containing skaters' data.
    - num (int): The number of top hitters to display.

    Returns:
    - names list
    """
    # Create a PlayerHandler instance
    hitters = PlayerHandler(sdf)
    # Get the top hitters using the PlayerHandler instance
    top_hitters = hitters.top_players_by_hits(num)
    top_hitters.index = range(1,len(top_hitters) + 1)
    # Print information about the top hitters
    print("\nTop Hitters:")
    for index, row in top_hitters.iterrows():
        print(f"Top Hitters #:{index} {row['Player Name']} from {row['Team Name']} has {row['Hits']} Hits.")
    return hitters

def penalty_minutes_analysis(sdf, num):
    """
    Analyzes skaters' data and prints players with the highest penalty minutes.

    Parameters:
    - sdf (pandas.DataFrame): DataFrame containing skaters' data.
    - num (int): The number of players with the highest penalty minutes to display.

    Returns:
    - names list
    """
    # Create a PlayerHandler instance
    penalty = PlayerHandler(sdf)
    # Get players with the highest penalty minutes using the PlayerHandler instance
    top_penalty_minutes = penalty.top_players_by_pim(num)
    top_penalty_minutes.index = range(1,len(top_penalty_minutes) + 1)
    # Print information about players with the highest penalty minutes
    print("\nPlayers with the Highest Penalty Minutes:")
    for index, row in top_penalty_minutes.iterrows():
        print(f"Top Penalty Minutes #:{index} {row['Player Name']} from {row['Team Name']} has {row['PIM']} minutes.")
    return penalty

def skaters_analysis(sdf):
    """
    Analyzes skaters' data and prints the top 10 goal scorers.

    Parameters:
    - sdf (pandas.DataFrame): DataFrame containing skaters' data.

    Returns:
    - None
    """
    # Create a PlayerHandler instance
    skaters = PlayerHandler(sdf)
    # Create a copy of the skaters' DataFrame
    skaters_df = sdf.copy()
    # Calculate points by adding goals (G) and assists (A)
    skaters_df['Points'] = skaters_df['G'] + skaters_df['A']
    # Get the top 10 goal scorers based on points
    top_goal_scorers = skaters_df.sort_values(by='Points', ascending=False).head(10)
    # Print information about the top 10 goal scorers
    print("\nTop 10 Goal Scorers:")
    print(top_goal_scorers[['Player Name', 'Points']])

def parse_args(arglist):
    """
    Parses command-line arguments for the NHL Stats Analyzer.

    Parameters:
    - arglist (list): List of command-line arguments.

    Returns:
    - Namespace: An object containing attributes corresponding to the command-line arguments.
    """
    # Create an ArgumentParser instance with a description
    parser = ArgumentParser(description="NHL Stats Analyzer")
    
    # Add command-line arguments for different analysis options
    parser.add_argument('-tgs', '--topgoalscorers', nargs=1, type=int, help="Show Top Goal Scorers (include n scorers)")
    parser.add_argument('-bg', '--bestgoalies', nargs=1, type=int, help="Show Best Goalies (include n goalies)")
    parser.add_argument('-bh', '--biggesthitters', nargs=1, type=int, help="Show Biggest Hitters (include n hitters)")
    parser.add_argument('-pm', '--penaltyminutes', nargs=1, type=int, help="Show Players With Highest Penalty Minutes")
    
    # Parse the command-line arguments and return the result
    return parser.parse_args(arglist)

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args(sys.argv[1:])

    # Read skaters data from CSV file and add 'Team Name' column
    skaters_df = pd.read_csv("nhl-stats_1.csv", skiprows=1)
    #skaters_df['Team Name'] = skaters_df['Team'].map(nhl_teams)

    # Read goalies data from CSV file and add 'Team Name' column
    goalies_df = pd.read_csv("nhl-stats_2.csv", skiprows=1)
    #goalies_df['Team Name'] = goalies_df['Team'].map(nhl_teams)

    # Perform analysis based on user's command-line arguments
    if args.topgoalscorers:
        num = args.topgoalscorers[0]
        print(f"Processing Top {num} Goal Scorers...")
        goal_scorers_analysis(skaters_df, num)
    elif args.bestgoalies:
        num = args.bestgoalies[0]
        print(f"Processing Best {num} Goalies...")
        goalies_analysis(goalies_df, num)
    elif args.biggesthitters:
        num = args.biggesthitters[0]
        print("Processing Biggest Hitters...")
        hitters_analysis(skaters_df, num)
    elif args.penaltyminutes:
        num = args.penaltyminutes[0]
        print("Processing Penalty Minutes Analysis...")
        penalty_minutes_analysis(skaters_df, num)
    else:
        print("Invalid choice. Please select a valid option.")
