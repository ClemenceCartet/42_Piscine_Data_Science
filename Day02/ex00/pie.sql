SELECT event_type, COUNT(event_type)
FROM customers.customersv3
GROUP BY event_type
ORDER BY COUNT(event_type) DESC;