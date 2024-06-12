SELECT date_trunc('month', event_time) AS month, SUM(price)
FROM customers.customersv3
WHERE event_type = 'purchase'
GROUP BY month;