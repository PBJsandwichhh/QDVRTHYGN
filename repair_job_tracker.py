import json
from dataclasses import dataclass, asdict
from datetime import date

@dataclass
class RepairJob:
    job_id: int
    customer_name: str
    item: str
    problem: str
    status: str = "Received"

    def summary(self):
        return f"[{self.job_id}] {self.customer_name} | {self.item} | {self.status}"

class RepairJobTracker:
    def __init__(self):
        self.jobs = []
        self.next_id = 1

    def add_job(self, customer_name, item, problem):
        job = RepairJob(
            self.next_id,
            customer_name,
            item,
            problem
        )
        self.jobs.append(job)
        self.next_id += 1
        return job

    def find_job(self, job_id):
        for job in self.jobs:
            if job.job_id == job_id:
                return job
        return None

    def update_status(self, job_id, new_status):
        job = self.find_job(job_id)
        if job:
            job.status = new_status
            return True
        return False

    def save(self, filename="repair_jobs.json"):
        with open(filename, "w", encoding="utf-8") as file:
            json.dump([asdict(job) for job in self.jobs], file, indent=4)

    def load(self, filename="repair_jobs.json"):
        try:
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.jobs = [RepairJob(**item) for item in data]
            self.next_id = max((job.job_id for job in self.jobs), default=0) + 1

        except FileNotFoundError:
            pass

def show_job(job):
    print("\n--- Repair Job ---")
    print(f"Job ID:     {job.job_id}")
    print(f"Customer:   {job.customer_name}")
    print(f"Item:       {job.item}")
    print(f"Problem:    {job.problem}")
    print(f"Status:     {job.status}")

def main():
    tracker = RepairJobTracker()
    tracker.load()

    while True:
        print("\n===== FIXTRACK PROTOTYPE =====")
        print("1. Add repair job")
        print("2. View repair jobs")
        print("3. Update job status")
        print("4. View job details")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            print("\n--- Add Repair Job ---")
            customer = input("Customer name: ").strip()
            item = input("Item being repaired: ").strip()
            problem = input("Reported problem: ").strip()

            if not customer or not item or not problem:
                print("Please fill in all fields.")
                continue

            job = tracker.add_job(customer, item, problem)
            tracker.save()
            print(f"Repair job #{job.job_id} added.")

        elif choice == "2":
            print("\n--- Repair Jobs ---")

            if not tracker.jobs:
                print("No repair jobs yet.")
                continue

            for job in tracker.jobs:
                print(job.summary())

        elif choice == "3":
            if not tracker.jobs:
                print("No repair jobs yet.")
                continue

            try:
                job_id = int(input("Enter job ID: "))
            except ValueError:
                print("Please enter a valid job ID.")
                continue

            job = tracker.find_job(job_id)

            if not job:
                print("Job not found.")
                continue

            print(f"Current status: {job.status}")
            print("1. Received")
            print("2. Diagnosing")
            print("3. Repairing")
            print("4. Ready for Pickup")
            print("5. Completed")

            status_choice = input("New status: ").strip()

            statuses = {
                "1": "Received",
                "2": "Diagnosing",
                "3": "Repairing",
                "4": "Ready for Pickup",
                "5": "Completed"
            }

            if status_choice in statuses:
                tracker.update_status(job_id, statuses[status_choice])
                tracker.save()
                print("Status updated.")
            else:
                print("Invalid status.")

        elif choice == "4":
            try:
                job_id = int(input("Enter job ID: "))
            except ValueError:
                print("Please enter a valid job ID.")
                continue

            job = tracker.find_job(job_id)

            if job:
                show_job(job)
            else:
                print("Job not found.")

        elif choice == "5":
            tracker.save()
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose 1–5.")

if __name__ == "__main__":
    main()