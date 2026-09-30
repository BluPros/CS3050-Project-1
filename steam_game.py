"""Steam game model and query-processing logic."""

from dataclasses import dataclass

from consts import RESULT_LIMIT


@dataclass
class SteamGame:
    """Represents one Steam game from a Firestore document."""

    app_id: int
    name: str
    release_year: int
    price: float
    genre: str
    has_metacritic: bool
    metacritic_url: str | None = None

    @classmethod
    def from_dict(cls, game_data):
        """Build a SteamGame object from a Firestore dictionary."""
        return cls(
            app_id=game_data["app_id"],
            name=game_data["name"],
            release_year=game_data["release_year"],
            price=game_data["price"],
            genre=game_data["genre"],
            has_metacritic=game_data["has_metacritic"],
            metacritic_url=game_data.get("metacritic_url"),
        )

    @classmethod
    def do_query(cls, parsed_query, connector):
        """
        Validate parsed query data, retrieve matching records, sort them,
        and return result text for the GUI.
        """
        cls.validate_query(parsed_query)

        first_condition = parsed_query["condition1"]
        second_condition = parsed_query.get("condition2")
        joiner = parsed_query.get("joiner")

        first_value = cls.convert_value(
            first_condition["field"],
            first_condition["value"],
        )

        if second_condition is None:
            records = connector.execute_single_filter(
                first_condition["field"],
                first_condition["operator"],
                first_value,
            )

        elif joiner.lower() == "and":
            second_value = cls.convert_value(
                second_condition["field"],
                second_condition["value"],
            )

            records = connector.execute_two_and_filters(
                first_condition["field"],
                first_condition["operator"],
                first_value,
                second_condition["field"],
                second_condition["operator"],
                second_value,
            )

        elif joiner.lower() == "or":
            records = cls.execute_or_query(
                connector,
                first_condition,
                second_condition,
            )

        else:
            raise ValueError(
                "Compound queries must use 'and' or 'or'."
            )

        games = [cls.from_dict(record) for record in records]
        sorted_games = cls.sort_games(games)

        return cls.format_results(sorted_games)

    @classmethod
    def validate_query(cls, parsed_query):
        """Check field/operator combinations after parsing syntax succeeds."""
        valid_fields = {
            "name",
            "genre",
            "release_year",
            "price",
            "has_metacritic",
        }

        valid_operators = {"==", "<", "<=", ">", ">="}

        conditions = [parsed_query["condition1"]]

        if parsed_query.get("condition2") is not None:
            conditions.append(parsed_query["condition2"])

        for condition in conditions:
            field = condition["field"]
            operator = condition["operator"]

            if field not in valid_fields:
                raise ValueError(
                    "Valid fields are: name, genre, release_year, "
                    "price, has_metacritic."
                )

            if operator not in valid_operators:
                raise ValueError(
                    "Valid operators are: ==, <, <=, >, >=."
                )

            if field in {"name", "genre", "has_metacritic"}:
                if operator != "==":
                    raise ValueError(
                        f"'{field}' may only use the == operator."
                    )

    @staticmethod
    def convert_value(field, raw_value):
        """Convert parser text to the type used by the Firestore document."""
        value = str(raw_value).strip()

        if field == "release_year":
            try:
                return int(value)
            except ValueError as error:
                raise ValueError(
                    "release_year must be a whole number, such as 2024."
                ) from error

        if field == "price":
            try:
                return float(value)
            except ValueError as error:
                raise ValueError(
                    "price must be a number, such as 0 or 19.99."
                ) from error

        if field == "has_metacritic":
            if value.lower() == "true":
                return True

            if value.lower() == "false":
                return False

            raise ValueError(
                "has_metacritic must be either true or false."
            )

        return value

    @classmethod
    def execute_or_query(cls, connector, first_condition, second_condition):
        """Run two single-condition queries and merge unique results."""
        first_records = connector.execute_single_filter(
            first_condition["field"],
            first_condition["operator"],
            cls.convert_value(
                first_condition["field"],
                first_condition["value"],
            ),
        )

        second_records = connector.execute_single_filter(
            second_condition["field"],
            second_condition["operator"],
            cls.convert_value(
                second_condition["field"],
                second_condition["value"],
            ),
        )

        unique_records = {}

        for record in first_records + second_records:
            unique_records[record["app_id"]] = record

        return list(unique_records.values())

    @staticmethod
    def sort_games(games):
        """Sort result objects alphabetically by name."""
        return sorted(
            games,
            key=lambda game: (
                game.name.casefold(),
                game.release_year,
                game.app_id,
            ),
        )

    @classmethod
    def format_results(cls, games):
        """Return a user-readable results string for the GUI text box."""
        if not games:
            return "No matching Steam games were found."

        lines = [f"{len(games)} matching game(s):", ""]

        for game in games[:RESULT_LIMIT]:
            lines.append(game.to_display_string())

        if len(games) > RESULT_LIMIT:
            lines.append("")
            lines.append(
                f"Showing only the first {RESULT_LIMIT} results."
            )

        return "\n".join(lines)

    def to_display_string(self):
        """Produce one readable game result line."""
        price_text = "Free" if self.price == 0 else f"${self.price:.2f}"

        line = (
            f"{self.name} | "
            f"{self.release_year} | "
            f"{self.genre} | "
            f"{price_text}"
        )

        if self.metacritic_url:
            line += " | Metacritic available"

        return line