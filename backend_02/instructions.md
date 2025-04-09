# AI_INSTRUCTIONS.md

## General Guidelines
1. **Language & Frameworks:**
   - Use **Python 3.11+**.
   - Build the API using **FastAPI**.
   - Follow **PEP 8** (code style) and **PEP 257** (docstring conventions).

2. **Data Validation:**
   - **Pydantic** must be used for request/response validation and environment configuration.


3. **Deployment:**
   - Provide Docker support (via a Dockerfile and docker-compose configuration).


## API Design & Versioning
- All API routes should be prefixed with `/api/v1/`.
- Example endpoint: `POST /api/v1/{something}`



## Database Schema

### 1. Users Table
This table stores account information for all users (adopters, individual pet owners, shelter representatives, and admins).

- **user_id** (PK): Unique identifier for each user.
- **username**: User's chosen name.
- **email**: User's email address.
- **password**: password 
- **role**: User role (ENUM: `'adopter'`, `'individual'`, `'shelter'`, `'admin'`).
- **created_at**: Timestamp when the account was created.

### 2. User_Profiles Table
Contains additional details about a user, which can be used for contact information and extended profile data.

- **profile_id** (PK): Unique identifier for each profile.
- **user_id** (FK): References the Users table.
- **full_name**: User's full name.
- **phone_number**: Contact number.
- **address**: Physical address.
- **additional_info**: JSON field for extra details (e.g. shelter name, description).
- **updated_at**: Timestamp of last profile update.

### 3. Pets Table
Stores information about each pet listed for adoption. This table is central to tracking who posted the pet and its details.

- **pet_id** (PK): Unique identifier for each pet.
- **owner_id** (FK): References the Users table (this field tracks who submitted the listing).
- **owner_type**: ENUM field indicating whether the pet was submitted by a `'shelter'` or an `'individual'`.  
- **name**: Pet's name.
- **pet_type_id** (FK): References the Pet_Types table.
- **breed_id** (FK): References the Breeds table.
- **age**: Pet's age.
- **gender**: Pet's gender.
- **description**: Detailed information about the pet.
- **image_url**: URL linking to the pet's image.
- **status**: Adoption status (ENUM: `'available'`, `'pending'`, `'adopted'`).
- **created_at**: Timestamp when the pet was listed.

### 4. Pet_Types Table
Defines the types of pets available on the platform.

- **pet_type_id** (PK): Unique identifier for each pet type.
- **type_name**: Name of the pet type (e.g. Dog, Cat, Rabbit).

### 5. Breeds Table
Lists the various breeds associated with each pet type.

- **breed_id** (PK): Unique identifier for each breed.
- **pet_type_id** (FK): References the Pet_Types table.
- **breed_name**: Name of the breed.

### 6. Adoption_Applications Table
Records adoption applications submitted by potential adopters.

- **application_id** (PK): Unique identifier for each application.
- **pet_id** (FK): References the Pets table.
- **adopter_id** (FK): References the Users table (the user applying for adoption).
- **message**: Optional message from the adopter.
- **status**: Application status (ENUM: `'submitted'`, `'approved'`, `'rejected'`).
- **submitted_at**: Timestamp when the application was submitted.

### 7. Success_Stories Table
Stores stories or testimonials from successful adoptions.

- **story_id** (PK): Unique identifier for each story.
- **pet_id** (FK): References the Pets table.
- **adopter_id** (FK): References the Users table (person who adopted).
- **story_title**: Title of the story.
- **story_content**: Detailed narrative.
- **image_url**: URL for an image related to the story.
- **published_at**: Timestamp when the story was published.

### 8. Resources Table
Holds pet care articles, training guides, and other resources.

- **resource_id** (PK): Unique identifier for each resource.
- **title**: Title of the resource.
- **content**: Detailed content or link.
- **category**: Resource category (e.g. `'Care Tips'`, `'Training Guides'`).
- **author_id** (FK): References Users table if resources are user-generated.
- **published_at**: Timestamp of publication.

### 9. Visit_Schedules Table
Enables potential adopters to schedule visits to meet a pet.

- **visit_id** (PK): Unique identifier for each visit scheduling entry.
- **pet_id** (FK): References the Pets table.
- **adopter_id** (FK): References the Users table (the one scheduling the visit).
- **scheduled_date**: The date and time for the visit.
- **status**: Status of the visit request (ENUM: `'pending'`, `'confirmed'`, `'completed'`, `'cancelled'`).
- **message**: Optional message from the adopter.
- **created_at**: Timestamp when the visit was scheduled.

---

## Backend API Endpoints

The API follows RESTful design principles and is grouped by functionality.

### Authentication & User Management

- **POST /api/register**  
  *Registers a new user (adopter, individual, shelter representative).*  
  **Request Body:**  
  ```json
  {
    "username": "johndoe",
    "password": "securepassword",
    "email": "john@example.com",
    "role": "adopter", 
    "additional_info": {}
  }
  ```  
  **Response:**  
  - `201 Created`: User registered.
  - `400 Bad Request`: Invalid input.

- **POST /api/login**  
  *Authenticates a user and returns a JWT token.*  
  **Request Body:**  
  ```json
  {
    "username": "johndoe",
    "password": "securepassword"
  }
  ```  
  **Response:**  
  - `200 OK`: Returns token.
  - `401 Unauthorized`: Invalid credentials.

- **GET /api/users/{user_id}**  
  *Retrieves user details.*  
  **Response:**  
  - `200 OK`: Returns user information.
  - `404 Not Found`: User not found.

- **PUT /api/users/{user_id}**  
  *Updates user details.*  
  **Request Body:** (fields to update)  
  **Response:**  
  - `200 OK`: User updated.
  - `400 Bad Request`/`404 Not Found`: On errors.

### Pet Management

- **POST /api/pets**  
  *Creates a new pet listing (shelters or individual users).*  
  **Request Body:**  
  ```json
  {
    "name": "Buddy",
    "pet_type_id": 1,
    "breed_id": 5,
    "age": 3,
    "gender": "Male",
    "description": "Friendly and energetic.",
    "image_url": "http://example.com/buddy.jpg",
    "owner_id": 10,
    "owner_type": "individual"  // or "shelter"
  }
  ```  
  **Response:**  
  - `201 Created`: Listing created.
  - `400 Bad Request`/`401 Unauthorized`: On error.

- **GET /api/pets**  
  *Retrieves all pet listings with optional filters (by type, breed, age, location etc.).*  
  **Query Parameters:** e.g. `pet_type`, `breed`, `status`  
  **Response:**  
  - `200 OK`: List of pets.

- **GET /api/pets/{pet_id}**  
  *Retrieves details of a specific pet listing.*  
  **Response:**  
  - `200 OK`: Returns pet details.
  - `404 Not Found`: Pet not found.

- **PUT /api/pets/{pet_id}**  
  *Updates a specific pet listing (only allowed by the owner or an admin).*  
  **Request Body:** (fields to update)  
  **Response:**  
  - `200 OK`: Updated.
  - `400 Bad Request`/`401 Unauthorized`/`404 Not Found`: On error.

- **DELETE /api/pets/{pet_id}**  
  *Deletes a pet listing (only allowed by the owner or an admin).*  
  **Response:**  
  - `200 OK`: Listing deleted.
  - `401 Unauthorized`/`404 Not Found`: On error.

### Adoption Application Management

- **POST /api/adoptions**  
  *Submits a new adoption application for a pet.*  
  **Request Body:**  
  ```json
  {
    "pet_id": 15,
    "adopter_id": 10,
    "message": "I would love to provide a loving home."
  }
  ```  
  **Response:**  
  - `201 Created`: Application submitted.
  - `400 Bad Request`/`401 Unauthorized`: On error.

- **GET /api/adoptions**  
  *Retrieves all adoption applications for the authenticated user (adopters view their submissions; shelter/individual owners view applications for their pets).*  
  **Response:**  
  - `200 OK`: List of applications.

- **GET /api/adoptions/{application_id}**  
  *Retrieves details of a specific adoption application.*  
  **Response:**  
  - `200 OK`: Application details.
  - `404 Not Found`: Application not found.

- **PUT /api/adoptions/{application_id}**  
  *Updates the status of an adoption application (e.g. approved, rejected), allowed for shelter representatives or the pet owner.*  
  **Request Body:**  
  ```json
  {
    "status": "approved"
  }
  ```  
  **Response:**  
  - `200 OK`: Application updated.
  - `400 Bad Request`/`404 Not Found`: On error.

### Success Stories Management

- **POST /api/stories**  
  *Submits a new success story (with moderation if required).*  
  **Request Body:**  
  ```json
  {
    "pet_id": 15,
    "adopter_id": 10,
    "story_title": "Our Happy Ending",
    "story_content": "We found our best friend...",
    "image_url": "http://example.com/story.jpg"
  }
  ```  
  **Response:**  
  - `201 Created`: Story submitted.
  - `400 Bad Request`/`401 Unauthorized`: On error.

- **GET /api/stories**  
  *Retrieves all success stories.*  
  **Response:**  
  - `200 OK`: List of stories.

- **GET /api/stories/{story_id}**  
  *Retrieves a specific success story.*  
  **Response:**  
  - `200 OK`: Story details.
  - `404 Not Found`: Not found.

- **PUT /api/stories/{story_id}**  
  *Updates a success story (allowed for the story owner or admin).*  
  **Response:**  
  - `200 OK`: Story updated.
  - `400/401/404`: On error.

- **DELETE /api/stories/{story_id}**  
  *Deletes a success story (allowed for the story owner or admin).*  
  **Response:**  
  - `200 OK`: Story deleted.
  - `401/404`: On error.

### Resources & Guides Management

- **POST /api/resources**  
  *Creates a new resource article (for pet care, training, etc.).*  
  **Request Body:**  
  ```json
  {
    "title": "How to Care for Your New Puppy",
    "content": "Detailed article content here...",
    "category": "Care Tips",
    "author_id": 10
  }
  ```  
  **Response:**  
  - `201 Created`: Resource created.
  - `400 Bad Request`/`401 Unauthorized`: On error.

- **GET /api/resources**  
  *Retrieves all resource articles, optionally filtered by category.*  
  **Response:**  
  - `200 OK`: List of resources.

- **GET /api/resources/{resource_id}**  
  *Retrieves a specific resource article.*  
  **Response:**  
  - `200 OK`: Resource details.
  - `404 Not Found`: Not found.

- **PUT /api/resources/{resource_id}**  
  *Updates a resource article (allowed for the author or admin).*  
  **Response:**  
  - `200 OK`: Resource updated.
  - `400/401/404`: On error.

- **DELETE /api/resources/{resource_id}**  
  *Deletes a resource article (allowed for the author or admin).*  
  **Response:**  
  - `200 OK`: Resource deleted.
  - `401/404`: On error.

### Visit Scheduling Management

- **POST /api/visits**  
  *Schedules a visit for a pet, enabling adopters to request a meeting.*  
  **Request Body:**  
  ```json
  {
    "pet_id": 15,
    "adopter_id": 10,
    "scheduled_date": "2025-04-10T14:00:00Z",
    "message": "I would like to meet Buddy to see if we're a good match."
  }
  ```  
  **Response:**  
  - `201 Created`: Visit request submitted.
  - `400 Bad Request`/`401 Unauthorized`: On error.

- **GET /api/visits**  
  *Retrieves visit schedules for the authenticated user. For pet owners, this lists requests for their pets; for adopters, it shows their scheduled visits.*  
  **Response:**  
  - `200 OK`: List of scheduled visits.

- **GET /api/visits/{visit_id}**  
  *Retrieves details for a specific scheduled visit.*  
  **Response:**  
  - `200 OK`: Visit details.
  - `404 Not Found`: Not found.

- **PUT /api/visits/{visit_id}**  
  *Updates the status of a visit (e.g. confirming, completing, or cancelling a visit), allowed by the pet owner or admin.*  
  **Request Body:**  
  ```json
  {
    "status": "confirmed"
  }
  ```  
  **Response:**  
  - `200 OK`: Visit updated.
  - `400/404`: On error.

- **DELETE /api/visits/{visit_id}**  
  *Cancels a scheduled visit (by the adopter or pet owner).*  
  **Response:**  
  - `200 OK`: Visit cancelled.
  - `401/404`: On error.

---


Use Supabase as a Database