from app import create_app
from models import db, Student, generate_student_id
from datetime import date

app = create_app()

students_data = [
    # Batch 1 — original 10
    {
        "first_name": "Emma", "last_name": "Johnson",
        "dob": date(2003, 4, 12), "gender": "female",
        "email": "emma.johnson@email.com", "phone": "+1 415 555 0101",
        "street": "123 Oak Street", "city": "San Francisco", "state": "California",
        "zip_code": "94102", "country": "United States",
        "high_school": "Lincoln High School", "graduation_year": 2021,
        "major": "computer_science", "enrollment_type": "full_time",
        "password": "Emma@1234",
    },
    {
        "first_name": "Liam", "last_name": "Williams",
        "dob": date(2002, 8, 23), "gender": "male",
        "email": "liam.williams@email.com", "phone": "+1 213 555 0202",
        "street": "456 Maple Ave", "city": "Los Angeles", "state": "California",
        "zip_code": "90001", "country": "United States",
        "high_school": "Jefferson High School", "graduation_year": 2020,
        "major": "data_science", "enrollment_type": "full_time",
        "password": "Liam@1234",
    },
    {
        "first_name": "Sophia", "last_name": "Brown",
        "dob": date(2004, 1, 5), "gender": "female",
        "email": "sophia.brown@email.com", "phone": "+1 312 555 0303",
        "street": "789 Pine Road", "city": "Chicago", "state": "Illinois",
        "zip_code": "60601", "country": "United States",
        "high_school": "Northside Prep", "graduation_year": 2022,
        "major": "psychology", "enrollment_type": "part_time",
        "password": "Sophia@1234",
    },
    {
        "first_name": "Noah", "last_name": "Davis",
        "dob": date(2001, 11, 17), "gender": "male",
        "email": "noah.davis@email.com", "phone": "+1 512 555 0404",
        "street": "321 Elm Street", "city": "Austin", "state": "Texas",
        "zip_code": "73301", "country": "United States",
        "high_school": "Austin High School", "graduation_year": 2019,
        "major": "software_engineering", "enrollment_type": "full_time",
        "password": "Noah@1234",
    },
    {
        "first_name": "Olivia", "last_name": "Martinez",
        "dob": date(2003, 6, 30), "gender": "female",
        "email": "olivia.martinez@email.com", "phone": "+1 305 555 0505",
        "street": "654 Cedar Blvd", "city": "Miami", "state": "Florida",
        "zip_code": "33101", "country": "United States",
        "high_school": "Coral Gables High", "graduation_year": 2021,
        "major": "business_admin", "enrollment_type": "full_time",
        "password": "Olivia@1234",
    },
    {
        "first_name": "Ethan", "last_name": "Garcia",
        "dob": date(2002, 3, 14), "gender": "male",
        "email": "ethan.garcia@email.com", "phone": "+1 602 555 0606",
        "street": "987 Birch Lane", "city": "Phoenix", "state": "Arizona",
        "zip_code": "85001", "country": "United States",
        "high_school": "Desert Vista High", "graduation_year": 2020,
        "major": "cybersecurity", "enrollment_type": "part_time",
        "password": "Ethan@1234",
    },
    {
        "first_name": "Ava", "last_name": "Wilson",
        "dob": date(2004, 9, 8), "gender": "female",
        "email": "ava.wilson@email.com", "phone": "+1 206 555 0707",
        "street": "147 Spruce Way", "city": "Seattle", "state": "Washington",
        "zip_code": "98101", "country": "United States",
        "high_school": "Garfield High School", "graduation_year": 2022,
        "major": "graphic_design", "enrollment_type": "full_time",
        "password": "Ava@1234",
    },
    {
        "first_name": "James", "last_name": "Anderson",
        "dob": date(2001, 7, 22), "gender": "male",
        "email": "james.anderson@email.com", "phone": "+1 617 555 0808",
        "street": "258 Walnut St", "city": "Boston", "state": "Massachusetts",
        "zip_code": "02101", "country": "United States",
        "high_school": "Boston Latin School", "graduation_year": 2019,
        "major": "mathematics", "enrollment_type": "full_time",
        "password": "James@1234",
    },
    {
        "first_name": "Isabella", "last_name": "Taylor",
        "dob": date(2003, 12, 3), "gender": "female",
        "email": "isabella.taylor@email.com", "phone": "+1 404 555 0909",
        "street": "369 Peach Tree Dr", "city": "Atlanta", "state": "Georgia",
        "zip_code": "30301", "country": "United States",
        "high_school": "Westlake High School", "graduation_year": 2021,
        "major": "nursing", "enrollment_type": "full_time",
        "password": "Isabella@1234",
    },
    {
        "first_name": "Lucas", "last_name": "Thomas",
        "dob": date(2002, 5, 19), "gender": "male",
        "email": "lucas.thomas@email.com", "phone": "+1 720 555 1010",
        "street": "741 Mountain View", "city": "Denver", "state": "Colorado",
        "zip_code": "80201", "country": "United States",
        "high_school": "East High School", "graduation_year": 2020,
        "major": "mechanical_eng", "enrollment_type": "part_time",
        "password": "Lucas@1234",
    },
    # Batch 2 — additional 10
    {
        "first_name": "Mia", "last_name": "Jackson",
        "dob": date(2003, 2, 28), "gender": "female",
        "email": "mia.jackson@email.com", "phone": "+1 503 555 1111",
        "street": "852 Fern Ave", "city": "Portland", "state": "Oregon",
        "zip_code": "97201", "country": "United States",
        "high_school": "Lincoln High Portland", "graduation_year": 2021,
        "major": "electrical_eng", "enrollment_type": "full_time",
        "password": "Mia@1234",
    },
    {
        "first_name": "Benjamin", "last_name": "White",
        "dob": date(2001, 10, 9), "gender": "male",
        "email": "benjamin.white@email.com", "phone": "+1 702 555 1212",
        "street": "963 Desert Rose Blvd", "city": "Las Vegas", "state": "Nevada",
        "zip_code": "89101", "country": "United States",
        "high_school": "Las Vegas Academy", "graduation_year": 2019,
        "major": "finance", "enrollment_type": "full_time",
        "password": "Benjamin@1234",
    },
    {
        "first_name": "Charlotte", "last_name": "Harris",
        "dob": date(2004, 7, 14), "gender": "female",
        "email": "charlotte.harris@email.com", "phone": "+1 615 555 1313",
        "street": "174 Music Row", "city": "Nashville", "state": "Tennessee",
        "zip_code": "37201", "country": "United States",
        "high_school": "Hillsboro High School", "graduation_year": 2022,
        "major": "marketing", "enrollment_type": "part_time",
        "password": "Charlotte@1234",
    },
    {
        "first_name": "Alexander", "last_name": "Lee",
        "dob": date(2002, 4, 25), "gender": "male",
        "email": "alexander.lee@email.com", "phone": "+1 808 555 1414",
        "street": "285 Aloha Street", "city": "Honolulu", "state": "Hawaii",
        "zip_code": "96801", "country": "United States",
        "high_school": "Punahou School", "graduation_year": 2020,
        "major": "civil_eng", "enrollment_type": "full_time",
        "password": "Alexander@1234",
    },
    {
        "first_name": "Amelia", "last_name": "Clark",
        "dob": date(2003, 9, 17), "gender": "female",
        "email": "amelia.clark@email.com", "phone": "+1 907 555 1515",
        "street": "396 Aurora Drive", "city": "Anchorage", "state": "Alaska",
        "zip_code": "99501", "country": "United States",
        "high_school": "West High School AK", "graduation_year": 2021,
        "major": "biology", "enrollment_type": "full_time",
        "password": "Amelia@1234",
    },
    {
        "first_name": "Henry", "last_name": "Lewis",
        "dob": date(2001, 6, 3), "gender": "male",
        "email": "henry.lewis@email.com", "phone": "+1 505 555 1616",
        "street": "507 Adobe Way", "city": "Albuquerque", "state": "New Mexico",
        "zip_code": "87101", "country": "United States",
        "high_school": "Manzano High School", "graduation_year": 2019,
        "major": "architecture", "enrollment_type": "part_time",
        "password": "Henry@1234",
    },
    {
        "first_name": "Evelyn", "last_name": "Robinson",
        "dob": date(2004, 11, 21), "gender": "female",
        "email": "evelyn.robinson@email.com", "phone": "+1 919 555 1717",
        "street": "618 Research Triangle Pkwy", "city": "Raleigh", "state": "North Carolina",
        "zip_code": "27601", "country": "United States",
        "high_school": "Broughton High School", "graduation_year": 2022,
        "major": "chemistry", "enrollment_type": "full_time",
        "password": "Evelyn@1234",
    },
    {
        "first_name": "Sebastian", "last_name": "Walker",
        "dob": date(2002, 1, 30), "gender": "male",
        "email": "sebastian.walker@email.com", "phone": "+1 317 555 1818",
        "street": "729 Circle City Ave", "city": "Indianapolis", "state": "Indiana",
        "zip_code": "46201", "country": "United States",
        "high_school": "Pike High School", "graduation_year": 2020,
        "major": "film_media", "enrollment_type": "part_time",
        "password": "Sebastian@1234",
    },
    {
        "first_name": "Harper", "last_name": "Hall",
        "dob": date(2003, 8, 6), "gender": "female",
        "email": "harper.hall@email.com", "phone": "+1 502 555 1919",
        "street": "840 Bluegrass Blvd", "city": "Louisville", "state": "Kentucky",
        "zip_code": "40201", "country": "United States",
        "high_school": "Manual High School KY", "graduation_year": 2021,
        "major": "english", "enrollment_type": "full_time",
        "password": "Harper@1234",
    },
    {
        "first_name": "Daniel", "last_name": "Young",
        "dob": date(2001, 3, 11), "gender": "male",
        "email": "daniel.young@email.com", "phone": "+1 401 555 2020",
        "street": "951 Ocean State Dr", "city": "Providence", "state": "Rhode Island",
        "zip_code": "02901", "country": "United States",
        "high_school": "Classical High School", "graduation_year": 2019,
        "major": "physics", "enrollment_type": "full_time",
        "password": "Daniel@1234",
    },
]

with app.app_context():
    added = 0
    skipped = 0
    for data in students_data:
        if Student.query.filter_by(email=data["email"]).first():
            print(f"  SKIP  {data['email']} (already exists)")
            skipped += 1
            continue

        sid = generate_student_id()
        while Student.query.filter_by(student_id=sid).first():
            sid = generate_student_id()

        s = Student(
            student_id=sid,
            first_name=data["first_name"],
            last_name=data["last_name"],
            dob=data["dob"],
            gender=data["gender"],
            email=data["email"],
            phone=data["phone"],
            street=data["street"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
            country=data["country"],
            high_school=data["high_school"],
            graduation_year=data["graduation_year"],
            major=data["major"],
            enrollment_type=data["enrollment_type"],
        )
        s.set_password(data["password"])
        db.session.add(s)
        print(f"  ADD   {s.student_id}  {s.full_name} — {s.major}")
        added += 1

    db.session.commit()
    print(f"\n✅  Done! {added} students added, {skipped} skipped.")
    print(f"    Total students in DB: {Student.query.count()}")
