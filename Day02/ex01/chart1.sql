SELECT date_trunc('day', event_time) as day, COUNT(DISTINCT user_id)
FROM customers.customersv3
WHERE event_type = 'purchase'
GROUP BY day;