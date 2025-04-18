from experta import KnowledgeEngine, Rule, Fact, Field, MATCH
import pandas as pd

class Flight(Fact):
    flight_time = Field(int, mandatory=True)
    flight_capacity = Field(int, mandatory=True)
    flight_type = Field(str, mandatory=True)

class Cargo(Fact):
    cargo_weight = Field(int, mandatory=True)
    cargo_type = Field(str, mandatory=True)
    priority = Field(str, mandatory=True)

class SchedulingLogic(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.flight_schedules = []
        self.cargo_schedules = []

    @Rule(Flight(flight_time=MATCH.flight_time,
                 flight_capacity=MATCH.flight_capacity,
                 flight_type=MATCH.flight_type))
    def process_flight(self, flight_time, flight_capacity, flight_type):
        status = "Scheduled" if flight_time > 0 and flight_capacity > 0 else "Pending"
        self.flight_schedules.append({
            "flight_time": flight_time,
            "flight_capacity": flight_capacity,
            "flight_type": flight_type,
            "flight_status": status
        })

    @Rule(Cargo(cargo_weight=MATCH.cargo_weight,
                cargo_type=MATCH.cargo_type,
                priority=MATCH.priority))
    def process_cargo(self, cargo_weight, cargo_type, priority):
        status = "Scheduled" if cargo_weight > 0 else "Pending"
        self.cargo_schedules.append({
            "cargo_weight": cargo_weight,
            "cargo_type": cargo_type,
            "priority": priority,
            "cargo_status": status
        })

    def create_airline_schedule(self, flight_time, flight_capacity, flight_type):
        self.reset()
        self.declare(Flight(flight_time=flight_time,
                            flight_capacity=flight_capacity,
                            flight_type=flight_type))
        self.run()
        return self.flight_schedules[-1]

    def create_cargo_schedule(self, cargo_weight, cargo_type, priority):
        self.reset()
        self.declare(Cargo(cargo_weight=cargo_weight,
                           cargo_type=cargo_type,
                           priority=priority))
        self.run()
        return self.cargo_schedules[-1]

    def get_airline_schedule_summary(self):
        return pd.DataFrame(self.flight_schedules)

    def get_cargo_schedule_summary(self):
        return pd.DataFrame(self.cargo_schedules)
