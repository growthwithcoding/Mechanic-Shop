-- Create the Mechanic_Shop database
CREATE DATABASE IF NOT EXISTS Mechanic_Shop;

-- Create a dedicated user for the application
CREATE USER IF NOT EXISTS 'mechanic_user'@'localhost' IDENTIFIED BY 'mechanic_password';

-- Grant all privileges on the Mechanic_Shop database to the user
GRANT ALL PRIVILEGES ON Mechanic_Shop.* TO 'mechanic_user'@'localhost';

-- Apply the changes
FLUSH PRIVILEGES;

-- Show confirmation
SELECT 'Database and user created successfully!' AS Status;
