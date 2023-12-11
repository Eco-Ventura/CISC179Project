Medication Management System
Author: Fernando Valdivia
=====================================================
Version: 1.2
=====================================================
Version Changelog
1.0: Ability to create new clients and add medications to each file.
1.1: Added the ability to edit added medications
1.2: Added the ability to check if clients need refills on their medications.
1.21: Added some comments to main.py for better readability. 
Project Overview
This Python project assists facilities in managing their clients' medications using CSV files. It offers a simple and intuitive way to handle medication records, ensuring effective tracking and management.
=====================================================
Features
+Create New Client CSVs: Generate new CSV files for each client to store their medication data.
+Add, Delete, Modify, and Save Medications: Easily update medication details, add new entries, delete unnecessary ones, and save changes to the CSV files.
+Check for Upcoming Refills: Automatically identify medications that will need a refill within the next week, aiding in timely medication management.
=====================================================
CSV File Format

Each client's medication information is stored in a CSV file with the following format:

Medication,Daily Dose,Quantity,Last Count Date

Daily Dose: The amount of pills/capsules or doses taken per day. For example, if the medication is Gabapentin 300mg and the daily dose is 2, it indicates a total of 600mg per day, spread over two capsules.
Medication Strength: Include the strength of the medication in its name to facilitate ease of refill requests.
=====================================================
Note on HIPAA Compliance
As of the current version, this program is not HIPAA compliant due to the lack of end-to-end encryption for client information. It is recommended to use this program with caution and the understanding that it does not meet HIPAA standards for data privacy and security.
=====================================================
Future Plans
Explore options for implementing end-to-end encryption to ensure HIPAA compliance.
Continuous improvement based on user feedback and evolving requirements.
This project is a step towards streamlined and efficient medication management, aiming to support facilities in their healthcare endeavors.
=====================================================
