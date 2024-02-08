# csv_database.py - backup to database.py if MySQL cannot be resolved.

import csv
from dataStructures import Employee, Equipment, Skill


def write_employees_to_csv(employees, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Password Hashed", "Employee ID", "Contact Info", "Borrowed Equipment IDs", "Skill IDs", "Number of Lost Equipments", "Is Admin"])
        for employee in employees:
            writer.writerow([
                employee.name,
                employee.password_hash,
                employee.emp_id,
                employee.contactInfo,
                ",".join(employee.borrowedEquipIds),
                ",".join(employee.skillIds),
                employee.numLostEquips,
                employee.isAdmin
            ])

def read_employees_from_csv(filename):
    employees = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, password_hash, emp_id, contactInfo, borrowedEquipIds_str, skillIds_str, numLostEquips, isAdmin = row
            borrowedEquipIds = borrowedEquipIds_str.split(",") if borrowedEquipIds_str else []
            skillIds = skillIds_str.split(",") if skillIds_str else []
            employees.append(Employee(name, password_hash, emp_id, contactInfo, borrowedEquipIds, skillIds, int(numLostEquips), bool(isAdmin)))
    return employees


def write_equipment_to_csv(equipment, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Equipment ID", "Name", "Borrower ID", "Skill Requirements IDs", "Queue"])
        for equip in equipment:
            writer.writerow([
                equip.equipId,
                equip.name,
                equip.borrower_id,
                ",".join(equip.skillRequirementsIDs),
                ",".join(equip.queue)
            ])


def read_equipment_from_csv(filename):
    equipment = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            equip_id, name, borrower_id, skill_ids, queue = row
            skill_ids = skill_ids.split(",") if skill_ids else []
            queue = queue.split(",") if queue else []
            equipment.append(Equipment(
                equipId=equip_id,
                name=name,
                borrower_id=borrower_id if borrower_id != "None" else None,
                skillRequirementsIDs=skill_ids,
                queue=queue
            ))
    return equipment


def write_skills_to_csv(skills, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Skill ID"])
        for skill in skills:
            writer.writerow([
                skill.name,
                skill.skillId
            ])


def read_skills_from_csv(filename):
    skills = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            name, skill_id = row
            skills.append(Skill(
                name=name,
                skillId=skill_id
            ))
    return skills
