# API Endpoints Documentation

## **Storage Types Endpoints**

### **0. Base URI**
- **URI**: `https://4gt9bjtqq1.execute-api.eu-west-1.amazonaws.com/dev`


### **1. Create Storage Type**
- **Method**: `POST`
- **Path**: `/storage-types`
- **Authorization**: Required (`AdminCognitoAuthorizer`)

---

## **Storage Units Endpoints**

### **2. Create Storage Unit**
- **Method**: `POST`
- **Path**: `/storage-types/{typeId}/units`
- **Authorization**: Required (`AdminCognitoAuthorizer`)

### **3. Get Storage Units**
- **Method**: `GET`
- **Path**: `/units`
- **Authorization**: None

### **4. Update Storage Unit**
- **Method**: `PUT`
- **Path**: `/units/{unitId}`
- **Authorization**: Required (`AdminCognitoAuthorizer`)

### **5. Delete Storage Unit**
- **Method**: `DELETE`
- **Path**: `/units/{unitId}`
- **Authorization**: Required (`AdminCognitoAuthorizer`)

---

## **User Profile Endpoints**

### **6. Create or Update Profile**
- **Method**: `POST`
- **Path**: `/user/profile`
- **Authorization**: Required (`CognitoAuthorizer`)

### **7. Get User Profile**
- **Method**: `GET`
- **Path**: `/user/profile`
- **Authorization**: Required (`CognitoAuthorizer`)

---

## **Bookings Endpoints**

### **8. Create Booking**
- **Method**: `POST`
- **Path**: `/bookings`
- **Authorization**: Required (`CognitoAuthorizer`)

### **9. Get Customer Bookings**
- **Method**: `GET`
- **Path**: `/bookings`
- **Authorization**: Required (`CognitoAuthorizer`)

### **10. Update Booking**
- **Method**: `PUT`
- **Path**: `/bookings/{bookingId}`
- **Authorization**: Required (`CognitoAuthorizer`)

### **11. Cancel Booking**
- **Method**: `PUT`
- **Path**: `/bookings/{bookingId}/cancel`
- **Authorization**: Required (`CognitoAuthorizer`)

### **12. Process Payment**
- **Method**: `POST`
- **Path**: `/bookings/{bookingId}/pay`
- **Authorization**: Required (`CognitoAuthorizer`)

---

## **Payment Methods Endpoints**

### **13. Manage Payment Methods**
- **Method**: `POST`
- **Path**: `/users/payment-methods`
- **Authorization**: Required (`CognitoAuthorizer`)
