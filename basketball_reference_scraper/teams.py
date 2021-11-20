import pandas as pd
from requests import get
from bs4 import BeautifulSoup
import numpy as np

try:
    from constants import TEAM_TO_TEAM_ABBR, TEAM_SETS
    from utils import remove_accents
except:
    from basketball_reference_scraper.constants import (
        TEAM_TO_TEAM_ABBR,
        TEAM_SETS,
    )
    from basketball_reference_scraper.utils import remove_accents


def get_roster(team, season_end_year):
    r = get(
        f"https://www.basketball-reference.com/teams/{team}/{season_end_year}.html"
    )
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]
        df.columns = [
            "NUMBER",
            "PLAYER",
            "POS",
            "HEIGHT",
            "WEIGHT",
            "BIRTH_DATE",
            "NATIONALITY",
            "EXPERIENCE",
            "COLLEGE",
        ]
        # remove rows with no player name (this was the issue above)
        df = df[df["PLAYER"].notna()]
        df["PLAYER"] = df["PLAYER"].apply(
            lambda name: remove_accents(name, team, season_end_year)
        )
        # handle rows with empty fields but with a player name.
        df["BIRTH_DATE"] = df["BIRTH_DATE"].apply(
            lambda x: pd.to_datetime(x) if pd.notna(x) else pd.NaT
        )
        df["NATIONALITY"] = df["NATIONALITY"].apply(
            lambda x: x.upper() if pd.notna(x) else ""
        )

    return df


def get_team_stats(team, season_end_year, data_format="PER_GAME"):
    if data_format == "TOTAL":
        selector = "div_totals-team"
    elif data_format == "PER_GAME":
        selector = "div_per_game-team"
    elif data_format == "PER_POSS":
        selector = "div_per_poss-team"
    elif data_format == "SHOOTING":
        selector = "div_shooting-team"
    r = get(
        f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}"
    )

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]

        if data_format == "SHOOTING":
            df.columns = df.columns.droplevel()
            df.drop(
                columns=[x for x in df.columns if "Unnamed" in x], inplace=True
            )
            if season_end_year >= 2022:
                df.columns = [
                    "Rk",
                    "Team",
                    "G",
                    "MP",
                    "FG%",
                    "Dist.",
                    "2P/FGA",
                    "0-3/FGA",
                    "3-10/FGA",
                    "10-16/FGA",
                    "16-3P/FGA",
                    "3P/FGA",
                    "2PPCT",
                    "0-3PCT",
                    "3-10PCT",
                    "10-16PCT",
                    "16-3PPCT",
                    "3PPCT",
                    "2PAssisted",
                    "3PAssisted",
                    "Dunks/FGA",
                    "DunkMade",
                    "LayupsFGA",
                    "LayupsMade",
                    "Corner3s/3PA",
                    "Corner3PCT",
                    "HeaveAttempts",
                    "HeavesMade",
                ]
            else:
                df.columns = [
                    "Rk",
                    "Team",
                    "G",
                    "MP",
                    "FG%",
                    "Dist.",
                    "2P/FGA",
                    "0-3/FGA",
                    "3-10/FGA",
                    "10-16/FGA",
                    "16-3P/FGA",
                    "3P/FGA",
                    "2PPCT",
                    "0-3PCT",
                    "3-10PCT",
                    "10-16PCT",
                    "16-3PPCT",
                    "3PPCT",
                    "2PAssisted",
                    "3PAssisted",
                    "Dunks/FGA",
                    "DunkMade",
                    "Corner3s/3PA",
                    "Corner3PCT",
                    "HeaveAttempts",
                    "HeavesMade",
                ]
                df["LayupsFGA"] = np.nan
                df["LayupsMade"] = np.nan

        df["Team"] = df["Team"].apply(lambda x: x.replace("*", "").upper())
        df["TEAM"] = df["Team"].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(["Rk", "Team"], axis=1)
        df.loc[
            :, "SEASON"
        ] = f"{season_end_year - 1}-{str(season_end_year)[2:]}"
        s = df[df["TEAM"] == team]
        return s


def get_opp_stats(team, season_end_year, data_format="PER_GAME"):
    if data_format == "TOTAL":
        selector = "div_totals-opponent"
    elif data_format == "PER_GAME":
        selector = "div_per_game-opponent"
    elif data_format == "PER_POSS":
        selector = "div_per_poss-opponent"
    elif data_format == "SHOOTING":
        selector = "div_shooting-opponent"
    r = get(
        f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fleagues%2FNBA_{season_end_year}.html&div={selector}"
    )

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]

        if data_format == "SHOOTING":
            df.columns = df.columns.droplevel()
            df.drop(
                columns=[x for x in df.columns if "Unnamed" in x], inplace=True
            )
            if season_end_year >= 2022:
                df.columns = [
                    "Rk",
                    "Team",
                    "G",
                    "MP",
                    "FG%",
                    "Dist.",
                    "2P/FGA",
                    "0-3/FGA",
                    "3-10/FGA",
                    "10-16/FGA",
                    "16-3P/FGA",
                    "3P/FGA",
                    "2PPCT",
                    "0-3PCT",
                    "3-10PCT",
                    "10-16PCT",
                    "16-3PPCT",
                    "3PPCT",
                    "2PAssisted",
                    "3PAssisted",
                    "Dunks/FGA",
                    "DunkMade",
                    "LayupsFGA",
                    "LayupsMade",
                    "Corner3s/3PA",
                    "Corner3PCT",
                ]
            else:
                df.columns = [
                    "Rk",
                    "Team",
                    "G",
                    "MP",
                    "FG%",
                    "Dist.",
                    "2P/FGA",
                    "0-3/FGA",
                    "3-10/FGA",
                    "10-16/FGA",
                    "16-3P/FGA",
                    "3P/FGA",
                    "2PPCT",
                    "0-3PCT",
                    "3-10PCT",
                    "10-16PCT",
                    "16-3PPCT",
                    "3PPCT",
                    "2PAssisted",
                    "3PAssisted",
                    "Dunks/FGA",
                    "DunkMade",
                    "Corner3s/3PA",
                    "Corner3PCT",
                ]
                df["LayupsFGA"] = np.nan
                df["LayupsMade"] = np.nan
        df["Team"] = df["Team"].apply(lambda x: x.replace("*", "").upper())
        df["TEAM"] = df["Team"].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(["Rk", "Team"], axis=1)
        df.columns = list(map(lambda x: "OPP_" + x, list(df.columns)))
        df.rename(columns={"OPP_TEAM": "TEAM"}, inplace=True)
        df.loc[
            :, "SEASON"
        ] = f"{season_end_year - 1}-{str(season_end_year)[2:]}"
        s = df[df["TEAM"] == team]
        return s


def get_team_misc(team, season_end_year):
    r = get(
        f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/leagues/NBA_{season_end_year}.html&div"
        f"=div_advanced-team"
    )
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df = pd.read_html(str(table))[0]
        df.columns = list(map(lambda x: x[1], list(df.columns)))
        df["Team"] = df["Team"].apply(lambda x: x.replace("*", "").upper())
        df["TEAM"] = df["Team"].apply(lambda x: TEAM_TO_TEAM_ABBR[x])
        df = df.drop(["Rk", "Team"], axis=1)
        df.rename(
            columns={
                "Age": "AGE",
                "Pace": "PACE",
                "Arena": "ARENA",
                "Attend.": "ATTENDANCE",
                "Attend./G": "ATTENDANCE/G",
            },
            inplace=True,
        )

        df.loc[
            :, "SEASON"
        ] = f"{season_end_year - 1}-{str(season_end_year)[2:]}"
        s = df[df["TEAM"] == team]
        s = s.loc[:, ~s.columns.str.contains("^Unnamed")]
        s.columns = [
            "AGE",
            "W",
            "L",
            "PW",
            "PL",
            "MOV",
            "SOS",
            "SRS",
            "ORtg",
            "DRtg",
            "NRtg",
            "PACE",
            "FTr",
            "3PAr",
            "TSPCT",
            "eFGPCT",
            "TOVPCT",
            "ORBPCT",
            "FT/FGA",
            "OppeFGPCT",
            "OppTOVPCT",
            "OppDRBPCT",
            "OppFT/FGA",
            "ARENA",
            "ATTENDANCE",
            "ATTENDANCE/G",
            "TEAM",
            "SEASON",
        ]
        return s


def get_roster_stats(
    team, season_end_year, data_format="PER_GAME", playoffs=False
):
    if playoffs:
        period = "playoffs"
    else:
        period = "leagues"
    selector = data_format.lower()

    if selector == "pbp":
        r = get(
            f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/{period}/NBA_{season_end_year}_play-by"
            f"-play.html&div=div_{selector}_stats"
        )
    else:
        r = get(
            f"https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/{period}/NBA_{season_end_year}_"
            f"{selector}.html&div=div_{selector}_stats"
        )
    df = None
    possible_teams = [team]

    for s in TEAM_SETS:
        if team in s:
            possible_teams = s
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        table = soup.find("table")
        df2 = pd.read_html(str(table))[0]
        if data_format in ["shooting"]:
            df2.columns = df2.columns.droplevel()
            df2 = df2.drop(columns=[x for x in df2.columns if "Unnamed" in x])
            df2.columns = [
                "Rk",
                "Player",
                "Pos",
                "Age",
                "Tm",
                "G",
                "MP",
                "FG%",
                "Dist.",
                "2P/FGA",
                "0-3/FGA",
                "3-10/FGA",
                "10-16/FGA",
                "16-3P/FGA",
                "3P/FGA",
                "2PPCT",
                "0-3PCT",
                "3-10PCT",
                "10-16PCT",
                "16-3PPCT",
                "3PPCT",
                "2PAssisted",
                "3PAssisted",
                "Dunks/FGA",
                "DunkAttempts",
                "Corner3s/3PA",
                "Corner3PPCT",
                "HeaveAttempts.",
                "HeavesMade",
            ]
        elif data_format == "pbp":
            df2.columns = df2.columns.droplevel()
            df2 = df2.drop(columns=[x for x in df2.columns if "Unnamed" in x])
            df2.columns = [
                "Rk",
                "Player",
                "Pos",
                "Age",
                "Tm",
                "G",
                "MP",
                "PGPCT",
                "SGPCT",
                "SFPCT",
                "PFPCT",
                "CPCT",
                "OnCourt",
                "On-Off",
                "BadPass",
                "LostBall",
                "ShootFoulCommitted",
                "OffFoulCommitted",
                "ShootFoulDrawn",
                "OffFoulDrawn",
                "PGA",
                "And1",
                "Blkd",
            ]

        for index, row in df2.iterrows():
            if row["Tm"] in possible_teams:
                if df is None:
                    df = pd.DataFrame(columns=list(row.index) + ["SEASON"])
                row[
                    "SEASON"
                ] = f"{season_end_year - 1}-{str(season_end_year)[2:]}"
                df = df.append(row)
        df.rename(
            columns={
                "Player": "PLAYER",
                "Age": "AGE",
                "Tm": "TEAM",
                "Pos": "POS",
            },
            inplace=True,
        )
        df["PLAYER"] = df["PLAYER"].apply(
            lambda name: remove_accents(name, team, season_end_year)
        )
        df = df.reset_index().drop(["Rk", "index"], axis=1)
        return df
