# Cloud Elective Capstone Project (Group 7)
## Storage Nook - Self-Storage Management Solution

Welcome to the **Storage Nook** project! This is a comprehensive solution for managing self-storage units, bookings, and financial analytics. The project includes a backend API built with AWS SAM (Serverless Application Model) and a frontend built using HTML, CSS, and JavaScript.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Storage Units Management](#storage-units-management)
  - [Bookings Management](#bookings-management)
  - [User Profiles](#user-profiles)
  - [Analytics](#analytics)
- [Frontend](#frontend)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Storage Nook is a serverless application designed for managing storage facilities. It allows administrators to manage storage units, view financial analytics, and handle user bookings efficiently. Customers can browse available units, book storage, and manage their profiles.

---

## Features

- **User Authentication**: Secure login and signup using AWS Cognito.
- **Storage Management**: Create, update, and delete storage units.
- **Bookings Management**: Customers can view, book, and cancel units.
- **Financial Analytics**: Admin dashboard with revenue, bookings, and occupancy statistics.
- **Responsive Frontend**: Easy-to-use interface for both admins and customers.

---

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: AWS Lambda, DynamoDB, API Gateway, Cognito
- **Infrastructure**: AWS SAM, CloudFormation

---

## Architecture

![Architecture Diagram](./architecture.png)

---

## Getting Started

### Prerequisites

- AWS CLI installed and configured.
- Node.js and NPM installed.
- SAM CLI installed (`pip install aws-sam-cli`).

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ssalidm/loud-elective-capstone-project-group-7.git
   cd cloud-elective-capstone-project-group-7

2. **Install dependencies**:
   ```bash
   cd Storage-Nook
   npm install

3. **Deploy backend**:
   ```bash
    cd storage-nook-backend
    cd users
    sam deploy --guided
    cd storage
    sam deploy --guided

# API Endpoints

## Authentication
| Method | Endpoint | Description |
|---|---|---|
| ```GET```  | ```/login```  | Redirect to cognito.  |
| ```GET```  | ```/signup```  | Redirect to cognito.  |

---

## Storage Units Management
| Method | Endpoint | Description |
|---|---|--|
| ```GET```  | ```/units```  | List all storage units..  |
| ```POST```  | ```/storage-types/<storage-type>/units```  | Create a new storage unit.  |
| ```PUT```  | ```/units/{unitId}```  | Update a storage unit.  |
| ```DELETE```  | ```/units/{unitId}```  | Delete a storage unit.  |


---

## Bookings Management
| Method | Endpoint | Description |
|---|---|--|
| ```GET```  | ```/bookings```  | List all bookings for a user.  |
| ```POST```  | ```/bookings```  | Create a new booking.  |
| ```PUT```  | ```/bookings/{bookingId}```  | Update a booking.  |
| ```DELETE```  | ```/bookings/{bookingId}```  | Delete a booking.  |

--- 

## User Profiles
| Method | Endpoint | Description |
|---|---|--|
| ```GET```  | ```user/profile```  | Get user profile.  |
| ```POST```  | ```user/profile```  | Create or Update user profile.  |

---

## Analytics
| Method | Endpoint | Description |
|---|---|--|
| ```GET```  | ```/analytics```  | Get financial analytics.  |
