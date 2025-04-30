***2025/04/29's push:***

1-the API for users CRUD's
      *THERAPIST:http://localhost:8001/auth/therapists/me/
      -PATIENT:http://localhost:8001/auth/patients/me/

2- to facilitate the THERAPIST creation precess (for tests), i sat the documents attribute as optional in the THERAPIST model, we can reset later.


***2025/04/29's 8:25PM push:*** -- Moncef

1- add additional field on User, Therapist models

2- add email verification using my email "selloummoncif.5@gmail.com" until we create a new one for the project.


***2025/04/30's 12:20PM push:*** -- Moncef

/matches/	Full access to all match records relevant to the user	Many matches	Authenticated users
/matches/me/	Manage the user's own (first) match	One match only	Authenticated users (patient or therapist)

1- Add a Match model and all its CRUDs (works perfectly)

2- idk what also but i think it's not important