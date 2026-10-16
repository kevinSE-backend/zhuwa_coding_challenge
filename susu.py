from decimal import Decimal, InvalidOperation
from collections import OrderedDict


class SusuGroup:
    def __init__(self, weekly_contribution):
        self.weekly_contribution = self._to_money(weekly_contribution)
        if self.weekly_contribution <= Decimal("0.00"):
            raise ValueError("Weekly contribution must be positive.")

        self.members = OrderedDict()
        self.current_week = 1
        self.contributions = {}
        self.payout_history = []

    @staticmethod
    def _to_money(amount):
        try:
            value = Decimal(str(amount))
        except (InvalidOperation, ValueError):
            raise ValueError("Invalid monetary amount.")

        if not value.is_finite():
            raise ValueError("Amount must be a finite number.")

        if value.as_tuple().exponent < -2:
            raise ValueError("Money cannot have more than two decimal places.")

        return value.quantize(Decimal("0.01"))

    def add_member(self, member_id):
        member_id = str(member_id).strip()

        if not member_id:
            raise ValueError("Member ID or name cannot be empty.")

        if member_id in self.members:
            raise ValueError("Member already exists.")

        self.members[member_id] = len(self.members) + 1

    def _validate_member(self, member_id):
        member_id = str(member_id).strip()

        if member_id not in self.members:
            raise ValueError("Unknown member.")

        return member_id

    def _get_contribution(self, member_id, week=None):
        week = self.current_week if week is None else week
        return self.contributions.get((week, member_id), Decimal("0.00"))

    def record_contribution(self, member_id, amount, week=None):
        member_id = self._validate_member(member_id)

        if week is not None and week != self.current_week:
            raise ValueError("Contributions can only be recorded for the current week.")

        amount = self._to_money(amount)

        if amount <= Decimal("0.00"):
            raise ValueError("Payment amount must be positive.")

        paid = self._get_contribution(member_id)
        owed = self.weekly_contribution - paid

        if amount > owed:
            raise ValueError(f"Payment exceeds the outstanding balance of GHS {owed:.2f}.")

        key = (self.current_week, member_id)
        self.contributions[key] = paid + amount

        return self.contributions[key]

    def close_week(self):
        if not self.members:
            raise ValueError("Cannot close a week without members.")

        outstanding = {}

        for member_id in self.members:
            paid = self._get_contribution(member_id)
            owed = self.weekly_contribution - paid

            if owed > Decimal("0.00"):
                outstanding[member_id] = owed

        if outstanding:
            return {
                "closed": False,
                "week": self.current_week,
                "outstanding": outstanding
            }

        pot = self.weekly_contribution * len(self.members)
        recipient = list(self.members.keys())[
            len(self.payout_history) % len(self.members)
        ]

        payout = {
            "week": self.current_week,
            "recipient": recipient,
            "amount": pot
        }

        self.payout_history.append(payout)
        self.current_week += 1

        return {
            "closed": True,
            "payout": payout,
            "next_week": self.current_week
        }

    def report(self):
        print("\n========== SUSU GROUP REPORT ==========")
        print(f"Weekly contribution: GHS {self.weekly_contribution:.2f}")
        print(f"Total members: {len(self.members)}")
        print(f"Current week: {self.current_week}")

        print("\nMember contributions:")

        if not self.members:
            print("No members registered.")

        for member_id in self.members:
            paid = self._get_contribution(member_id)
            owed = self.weekly_contribution - paid
            status = "Paid in full" if owed == 0 else "Outstanding"

            print(
                f"{member_id}: Paid GHS {paid:.2f}, "
                f"Owes GHS {owed:.2f}, Status: {status}"
            )

        print("\nPayout history:")

        if not self.payout_history:
            print("No payouts yet.")
        else:
            for payout in self.payout_history:
                print(
                    f"Week {payout['week']}: "
                    f"{payout['recipient']} received "
                    f"GHS {payout['amount']:.2f}"
                )

        print("=======================================\n")


def main():
    susu = SusuGroup("50.00")

    while True:
        print("1. Add member")
        print("2. Record contribution")
        print("3. Close week")
        print("4. Show report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                member_id = input("Enter member name or ID: ")
                susu.add_member(member_id)
                print("Member added successfully.")

            elif choice == "2":
                member_id = input("Enter member name or ID: ")
                amount = input("Enter payment amount in GHS: ")
                paid = susu.record_contribution(member_id, amount)
                print(f"Payment recorded. Total paid this week: GHS {paid:.2f}")

            elif choice == "3":
                result = susu.close_week()

                if result["closed"]:
                    payout = result["payout"]
                    print(
                        f"Week {payout['week']} closed successfully. "
                        f"{payout['recipient']} receives "
                        f"GHS {payout['amount']:.2f}."
                    )
                    print(f"Now entering week {result['next_week']}.")
                else:
                    print(f"Week {result['week']} cannot be closed.")
                    print("Outstanding contributions:")

                    for member_id, amount in result["outstanding"].items():
                        print(f"{member_id} owes GHS {amount:.2f}")

            elif choice == "4":
                susu.report()

            elif choice == "5":
                print("Goodbye.")
                break

            else:
                print("Invalid option. Please choose 1 to 5.")

        except ValueError as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()