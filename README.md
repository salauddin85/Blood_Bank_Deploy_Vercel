# Blood Bank Project

Welcome to the Blood Bank Project! This application serves as a platform for donors and recipients to connect, enabling users to manage blood donation requests and notifications effectively.

## Table of Contents
- [Features](#features)
- [User Roles](#user-roles)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Management**
  - User registration and login/logout functionality.
  - Profile viewing and updating.
  - Password change option.

- **Donation Notifications**
  - Users can send notifications for blood requests.
  - Active users can create events based on notifications.
  - Users can view available notifications.

- **Blog and Reviews**
  - Users can add blogs related to their donation experiences.
  - Users can leave reviews on their donation experience.

## User Roles

### Admin
The Admin has comprehensive control over the blood bank system. Admin capabilities include:
- Manage donors and recipients.
- View, accept, or cancel blood donation requests.
- Monitor user activity and maintain records.
- Manage notifications and events.

### Donor/User
The Donor (or User) can perform the following actions:
- Register and log in to the platform.
- Send notifications for blood donation requests.
- View available notifications from recipients.
- Create events based on received notifications.
- Add blogs related to their donation experiences.
- Leave reviews on their donation experience.
- Update their profile and change their password.


## API Endpoints

### Authentication
- **Register:**  
  `POST https://blood-bank-deploy-vercel.vercel.app/auth/register/`
- **Login:**  
  `POST https://blood-bank-deploy-vercel.vercel.app/auth/login/`
- **Logout:**  
  `POST https://blood-bank-deploy-vercel.vercel.app/auth/logout/`

### Donor Features
- **Notifications:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/notifications/`
- **Request User Donation Events:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/donation-events/`
- **Donation History:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/donation-history/`
- **All Donation Events:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/dashboard/`
- **Without Request User:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/dashboard/recipient_requests/`
- **All Donation History:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/events/dashboard/donation_history/`

### Other Features
- **About Us:**  
  `GET https://blood-bank-deploy-vercel.vercel.app/blood_bank_releted/about-us/`
- **Contact:**  
  `GET https://blood-bank-deploy-vercel.app/blood_bank_releted/contact/`
- **Blog:**  
  `GET https://blood-bank-deploy-vercel.app/blood_bank_releted/blog/`
- **Feedback:**  
  `POST https://blood-bank-deploy-vercel.app/blood_bank_releted/feedback/`
- **All Feedback:**  
  `GET https://blood-bank-deploy-vercel.app/blood_bank_releted/all_feedback/`
- **Subscriptions:**  
  `GET https://blood-bank-deploy-vercel.app/blood_bank_releted/subscriptions/`


## Getting Started

### Prerequisites

- Python 3.12.1
- Django 5.1
- Django Rest Framework

### Installation


### Setting Up the Django Environment on Windows

1. Create a virtual environment:
   ```bash
   python -m venv myenv
   ```

2. Navigate to the virtual environment directory:
   ```bash
   cd myenv
   ```

3. Activate the virtual environment:
   ```bash
   Scripts\Activate\myenv
   ```

4. To deactivate the virtual environment, use:
   ```bash
   deactivate
   ```

5. Install Django:
   ```bash
   pip install django
   ```

6. Create migrations:
   ```bash
   python manage.py makemigrations
   ```

7. Apply migrations:
   ```bash
   python manage.py migrate
   ```

8. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

9. Start the development server:
   ```bash
   python manage.py runserver
   ```
