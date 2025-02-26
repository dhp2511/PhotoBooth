# Photo-Booth

A responsive web-based photo album and sharing application with features like categorization, private/public galleries, and social interactions.

## Features
- 📸 Upload, edit, and delete photos
- 🔒 Private and public galleries
- 📂 Categorization for better organization
- 💬 Social interactions (likes/comments)
- 🌗 Light and Dark Theme Support
- ⚡ Optimized for performance with a lightweight backend

## Tech Stack
- **Frontend:** HTML, Bootstrap, JavaScript, HTMX
- **Backend:** Django
- **Database:** Supabase (postgres)
- **Deployment:** Render

## Screenshots

![image](https://github.com/user-attachments/assets/f9e02ef3-3a16-4222-a23b-6b688be7fa51)
![image](https://github.com/user-attachments/assets/2d60d8d7-cdbe-4f93-8f1d-019fe43ddd0d)
![image](https://github.com/user-attachments/assets/878668ef-0cfc-4279-9b7a-1438bac48776)


## Installation Local

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/Dhruvil2511/PhotoBooth.git
   cd PhotoBooth
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file and add necessary environment variables:
   ```sh
    DJANGO_SECRET_KEY = 
    EMAIL_HOST_USER =  
    EMAIL_HOST_PASSWORD =  
    CLOUDINARY_CLOUD_NAME =  
    CLOUDINARY_API_KEY =  
    CLOUDINARY_API_SECRET =  
    PGHOST =  
    PGPASSWORD =
    PGPORT =  
    GOOGLE_CLIENT_ID = 
    GOOGLE_SECRET_KEY =
    DJANGO_ENV = dev
    DJANGO_ALLOWED_HOSTS = 
   ```
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Run the development server:
   ```sh
   python manage.py runserver
   ```

## Usage
1. Open your browser and go to `http://127.0.0.1:8000/`
2. Register or log in to start using Photo-Booth
3. Upload and manage your photo collections
4. Interact with other users through likes and comments


---
### 📧 Contact
For any queries or suggestions, feel free to reach out via GitHub Issues.

