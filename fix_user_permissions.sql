-- Grant privileges for IPv6 localhost (::1)
CREATE USER IF NOT EXISTS 'mechanic_user'@'::1' IDENTIFIED BY 'mechanic_password';
GRANT ALL PRIVILEGES ON Mechanic_Shop.* TO 'mechanic_user'@'::1';

-- Grant privileges for IPv4 localhost (127.0.0.1)
CREATE USER IF NOT EXISTS 'mechanic_user'@'127.0.0.1' IDENTIFIED BY 'mechanic_password';
GRANT ALL PRIVILEGES ON Mechanic_Shop.* TO 'mechanic_user'@'127.0.0.1';

-- Apply the changes
FLUSH PRIVILEGES;

-- Show confirmation
SELECT 'Permissions updated for all localhost variants!' AS Status;
